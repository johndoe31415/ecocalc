#	ecocalc - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2017-2021 Johannes Bauer
#
#	This file is part of ecocalc.
#
#	ecocalc is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	ecocalc is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with ecocalc; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import sys
import re
import json
import fractions
import collections
from Recipe import Recipe, Resource
from Tools import NumberTools
from RecipeResolver import RecipeResolver

class Economy():
	_RecipeReference = collections.namedtuple("RecipeReference", [ "index", "recipe", "count" ])
	_RECIPE_DESCRIPTOR_RE = re.compile(r"((?P<cardinality>[\d/.]+)\s*(?P<percent>%)?)?\s*(?P<name_type>[#>]?)?(?P<name>[-_a-zA-Z0-9]+)")

	def __init__(self, args, eco_definition, additional_irreducible = None, excluded_recipe_indices = None):
		self._args = args
		self._def = eco_definition
		self._additional_irreducible = additional_irreducible
		self._excluded_recipe_indices = excluded_recipe_indices
		self._recipes = self._parse_recipes()
		self._recipes_by_name = { recipe.name: recipe for recipe in self._recipes if (recipe.name is not None) }
		self._resources = self._def["resources"]
		self._recipes_by_product = self._resolve_recipes_by_product()
		self._irreducible_resources = self._determine_irreducible_resources(additional_irreducible)
		self._preferred_recipe_by_product = self._get_preferred_recipes_by_product()
		self._plausibilize_resource_names()
		if self._args.verbose >= 3:
			self._print_debugging_info()

	def _print_debugging_info(self):
		print("Irreducible resources: %s" % (", ".join(sorted(self._irreducible_resources))))

	@property
	def all_recipes(self):
		return iter(self._recipes)

	def _plausibilize_resource_names(self):
		seen_resources = set()
		unknown_resources = set()
		for recipe in self._recipes:
			recipe_resources = recipe.resources
			for resource in recipe_resources:
				if resource in seen_resources:
					continue
				seen_resources.add(resource)
				pretty_name = self.get_resource_name(resource, surrogate = False)
				if pretty_name is None:
					print("Warning: Resource \"%s\" does not have a name defined (first referenced in recipe %s)." % (resource, recipe), file = sys.stderr)
					unknown_resources.add(resource)
		for resource_name in self._additional_irreducible:
			if resource_name not in seen_resources:
				print("Warning: Resource \"%s\" specified as irreducible, but resource is not known." % (resource_name), file = sys.stderr)
		if self._args.verbose >= 3:
			for resource in sorted(unknown_resources):
				pretty_name = resource.replace("_", " ")
				pretty_name = pretty_name[0].upper() + pretty_name[1:]
				print("		\"%s\": { \"name\": \"%s\" }," % (resource, pretty_name))

	def _parse_recipes(self):
		recipes = [ ]
		for (recipe_number, recipe) in enumerate(self._def["recipes"], 1):
			if "time" in recipe:
				cycle_time = NumberTools.str2num(recipe["time"])
			elif "rate" in recipe:
				cycle_time = 60 / NumberTools.str2num(recipe["rate"])
			else:
				cycle_time = None

			if "name" in recipe:
				name = "#%d: %s" % (recipe_number, recipe["name"])
			else:
				name = "#%d" % (recipe_number)
			produced_at = recipe.get("at")
			recipe = Recipe.from_str(recipe["recipe"], name = name, produced_at = produced_at, cycle_time = cycle_time)
			recipes.append(recipe)
		return recipes

	def _resolve_recipes_by_product(self):
		recipes_by_product = collections.defaultdict(list)
		for (recipe_index, recipe) in enumerate(self._recipes):
			for item in recipe.products:
				reference = self._RecipeReference(recipe = recipe, index = recipe_index, count = item.count)
				recipes_by_product[item.name].append(reference)
		return recipes_by_product

	def _get_preferred_recipes_by_product(self):
		preferred_recipes = { }
		for (product_name, recipes) in self._recipes_by_product.items():
			if product_name in self._irreducible_resources:
				# Ignore those where we deem resource irreducible
				continue
			preferred_recipe = None
			for recipe_ref in recipes:
				if recipe_ref.recipe.is_cyclic:
					continue
				if recipe_ref.index in self._excluded_recipe_indices:
					continue
				preferred_recipe = recipe_ref
				break

			if preferred_recipe is not None:
				preferred_recipes[product_name] = preferred_recipe
		return preferred_recipes

	def _determine_irreducible_resources(self, additional_irreducible):
		irreducible_resources = set()
		for (resource_name, resource) in self._resources.items():

			recipes = list(self.get_recipes_that_produce(resource_name))
			if len(recipes) == 0:
				# Resource that is never produced is irreducible, i.e., irreducible
				irreducible_resources.add(resource_name)

		if additional_irreducible is not None:
			irreducible_resources |= additional_irreducible
		return irreducible_resources

	def get_resource_name(self, internal_resource_name, surrogate = True):
		if (internal_resource_name in self._resources) and ("name" in self._resources[internal_resource_name]):
			return self._resources[internal_resource_name]["name"]
		else:
			if surrogate:
				return internal_resource_name
			else:
				return None

	def get_recipes_that_produce(self, internal_resource_name):
		return iter(self._recipes_by_product[internal_resource_name])

	def get_recipe_that_produces(self, internal_resource_name):
		return self._preferred_recipe_by_product.get(internal_resource_name)

	def get_recipe_by_descriptor(self, recipe_descriptor):
		match = self._RECIPE_DESCRIPTOR_RE.fullmatch(recipe_descriptor)
		if match is None:
			raise Exception("Not a valid recipe descriptor: %s" % (recipe_descriptor))
		match = match.groupdict()

		if match["cardinality"] is None:
			scalar = 1
		elif "/" in match["cardinality"]:
			# Fraction
			scalar = fractions.Fraction(match["cardinality"])
		else:
			# Integer or floating point value
			try:
				scalar = int(match["cardinality"])
			except ValueError:
				scalar = float(match["cardinality"])

		if match["percent"] is not None:
			scalar /= 100

		if match["name_type"] == "#":
			recipe_index = int(match["name"]) - 1
			if (recipe_index < 0) or (recipe_index >= len(self._recipes)):
				raise Exception("Invalid recipe number, must be between 1 and %d." % (len(self._recipes)))
			recipe = self._recipes[recipe_index]
		elif match["name_type"] == ">":
			recipe = Recipe((Resource(name = match["name"], count = scalar), ), (Resource(name = Recipe.FINISHED, count = 1), ), name = "Pseudo-Recipe")
			scalar = 1
		else:
			recipe = self._recipes_by_name[match["name"]]
		return recipe * scalar

	def all_ingredients_irreducible(self, recipe):
		for item in recipe.ingredients:
			if item.name not in self._irreducible_resources:
				return False
		return True

	def resolve_recursively(self, recipe):
		resolver = RecipeResolver(self)
		return resolver.recurse(recipe)

	def __getitem__(self, index):
		return self._recipes[index]

	@classmethod
	def from_args(cls, args):
		with open(args.ecofile) as f:
			eco_definition = json.load(f)
		additional_irreducible = set(args.consider_irreducible)
		excluded_recipe_indices = set((int(value) - 1) for value in args.exclude_recipe)
		return cls(args, eco_definition, additional_irreducible = additional_irreducible, excluded_recipe_indices = excluded_recipe_indices)
