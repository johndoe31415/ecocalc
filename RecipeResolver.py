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

import fractions
import itertools
import collections
from Recipe import Recipe

class ResolvedRecipe():
	_Application = collections.namedtuple("Application", [ "recipe_index", "recipe", "scalar", "pseudo_name" ])
	def __init__(self):
		self._recipe = Recipe.empty_recipe()
		self._applications = [ ]

	@property
	def recipe(self):
		return self._recipe

	@property
	def applications(self):
		return self._applications

	@property
	def grouped_applications(self):
		application_ref = { }
		by_recipe_index = collections.OrderedDict()
		for application in reversed(self.applications):
			if application.recipe_index is not None:
				application_ref[application.recipe_index] = application
				by_recipe_index[application.recipe_index] = by_recipe_index.get(application.recipe_index, 0) + application.scalar

		for (recipe_index, total_count) in by_recipe_index.items():
			application = application_ref[recipe_index]
			yield self._Application(recipe_index = application.recipe_index, recipe = application.recipe, scalar = total_count, pseudo_name = application.pseudo_name)

		for application in reversed(self.applications):
			if application.recipe_index is None:
				yield application

	def append(self, recipe_ref, scalar):
		self._recipe = self._recipe + (recipe_ref.recipe * scalar)
		self._applications.append(self._Application(recipe_index = recipe_ref.index, recipe = recipe_ref.recipe, scalar = scalar, pseudo_name = None))

	def append_pseudo_recipe(self, recipe, scalar = 1, name = None):
		self._recipe = self._recipe + (recipe * scalar)
		self._applications.append(self._Application(recipe_index = None, recipe = recipe, scalar = scalar, pseudo_name = name))

	def merge(self, resolved_recipe, scalar):
		self._recipe = self._recipe + (resolved_recipe.recipe * scalar)
		for application in resolved_recipe.applications:
			self._applications.append(self._Application(recipe_index = application.recipe_index, recipe = application.recipe, scalar = application.scalar * scalar, pseudo_name = application.pseudo_name))

	def __len__(self):
		return len(self._applications)

	def __str__(self):
		return "Producing {%s} by application of [%s]" % (self._recipe, self._applications)

class RecipeResolver():
	_DEBUG = False

	def __init__(self, eco):
		self._eco = eco
		self._resolved = { }

	def _log(self, msg):
		if self._DEBUG:
			print(msg)

	def _resolve_recipe(self, resolved_recipe):
		for resource in resolved_recipe.recipe.ingredients:
			resolved_ingredient = self._resolve_ingredient(resource.name)
			if resolved_ingredient is not None:
				resolved_recipe.merge(resolved_ingredient, resource.count)

	def _do_resolve_ingredient(self, ingredient_name):
		self._log("Resolving recipe that produces %s" % (ingredient_name))
		recipe_ref = self._eco.get_recipe_that_produces(ingredient_name)
		if recipe_ref is None:
			# Irreducible recipe
			return None

		# This is further decomposable
		resolved = ResolvedRecipe()
		resolved.append(recipe_ref, 1 / recipe_ref.count)
		self._resolve_recipe(resolved)
		return resolved

	def _resolve_ingredient(self, ingredient_name):
		if ingredient_name not in self._resolved:
			resolved = self._do_resolve_ingredient(ingredient_name)
			self._resolved[ingredient_name] = resolved
		return self._resolved[ingredient_name]

	def recurse(self, recipe, scalar = 1):
		self._log("Recusing into recipe: %s" % (str(recipe)))

		resolved_recipe = ResolvedRecipe()
		resolved_recipe.append_pseudo_recipe(recipe, scalar = scalar)
		self._resolve_recipe(resolved_recipe)
		return resolved_recipe
