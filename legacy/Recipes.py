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

import collections
from Recipe import Recipe
from Exceptions import ParseError
from RecipePath import RecipePath

class Recipes(object):
	def __init__(self):
		self._recipes = [ ]
		self._produces = collections.defaultdict(list)

	def add(self, recipe):
		self._recipes.append(recipe)
		self._produces[recipe.dest.item].append(recipe)

	def recipes_that_produce(self, item):
		return list(self._produces[item])

	@classmethod
	def parse_file(cls, filename):
		rcps = cls()
		with open(filename) as f:
			for (lineno, line) in enumerate(f, 1):
				line = line.rstrip("\r\n")
				if line.startswith("#") or line.strip() == "":
					continue
				try:
					recipe = Recipe.parse_line(line)
				except ParseError:
					raise Exception("Could not parse recipe on line %d." % (lineno))
				rcps.add(recipe)
		return rcps

	def __iter__(self):
		return iter(self._recipes)

	def dump(self):
		for recipe in self._recipes:
			print(recipe)

	def _paths(self, length = 1):
		if length == 1:
			for recipe in self:
				yield RecipePath.create_with_one_recipe(recipe)
		else:
			for recipe_path in self._paths(length - 1):
				yield from recipe_path.substitutions(self)

	def unique_paths(self, length = 1):
		unique = set()
		for path in self._paths(length):
			if path not in unique:
				yield path
				unique.add(path)

