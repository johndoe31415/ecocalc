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

import itertools

class RecipeResolution():
	def __init__(self, eco, recipe):
		self._eco = eco
		self._recipe = recipe
		self._substitutions = { }

	@property
	def sum_recipe(self):
		return self._recipe

	def __iter__(self):
		for (index, scalar) in sorted(self._substitutions.items()):
			recipe = self._eco[index]
			yield recipe * scalar

	def clone(self):
		clone = RecipeResolution(self._eco, self._recipe)
		clone._substitutions = dict(self._substitutions)
		return clone

	def apply(self, recipe_reference, source_scalar):
		scalar = source_scalar / recipe_reference.count
		clone = self.clone()
		clone._recipe = clone._recipe + (recipe_reference.recipe * scalar)
		clone._substitutions[recipe_reference.index] = clone._substitutions.get(recipe_reference.index, 0) + scalar
		return clone

	def recurse(self):
		yield self
		for item in self.sum_recipe.ingredients:
			candidates = self._eco.get_recipes_that_produce(item.name)
			for recipe_reference in candidates:
				substituted = self.apply(recipe_reference, item.count)
				yield from substituted.recurse()
