#	ecocalc - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2017-2020 Johannes Bauer
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

import re
import json
import fractions
from Recipe import Recipe
from Tools import NumberTools

class Economy():
	_RECIPE_DESCRIPTOR_RE = re.compile(r"((?P<cardinality>[\d/.]+)\s*(?P<percent>%)?)?\s*(?P<name>#?[-_a-zA-Z0-9]+)")

	def __init__(self, eco_definition, show_rate = False):
		self._def = eco_definition
		self._show_rate = show_rate
		self._recipes = self._parse_recipes()
		self._recipes_by_name = { recipe.name: recipe for recipe in self._recipes if (recipe.name is not None) }
		self._resources = self._def["resources"]

	@property
	def all_recipes(self):
		return iter(self._recipes)

	def _parse_recipes(self):
		recipes = [ ]
		for recipe in self._def["recipes"]:
			if self._show_rate:
				if "time" not in recipe:
					# We want rate-based recipes but this one doens't have a time defined. Ignore it.
					continue
				cycle_time = NumberTools.str2num(recipe["time"])
			else:
				cycle_time = None
			recipe = Recipe.from_str(recipe["recipe"], name = recipe.get("name"), cycle_time = cycle_time)
			recipes.append(recipe)
		return recipes

	def get_resource_name(self, internal_resource_name):
		if (internal_resource_name in self._resources) and ("name" in self._resources[internal_resource_name]):
			return self._resources[internal_resource_name]["name"]
		else:
			return internal_resource_name

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

		if match["name"].startswith("#"):
			recipe_index = int(match["name"][1:]) - 1
			recipe = self._recipes[recipe_index]
		else:
			recipe = self._recipes_by_name[match["name"]]
		return recipe.scale_by(scalar = scalar)

	@classmethod
	def from_file(cls, filename, show_rate = False):
		with open(filename) as f:
			eco_definition = json.load(f)
		return cls(eco_definition, show_rate = show_rate)
