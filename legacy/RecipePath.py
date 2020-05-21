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
import fractions
import collections
from Comparable import Comparable
from Items import Items

class RecipePath(Comparable):
	_PathStep = collections.namedtuple("PathStep", [ "cardinality", "recipe" ])
	def __init__(self, path):
		self._path = tuple(path)
		(self._src, self._dest) = self._calc_src_dest(self._path)

	def cmpkey(self):
		return ("recipepath", self._path)

	@classmethod
	def create_with_one_recipe(cls, recipe, cardinality = 1):
		path = ( cls._PathStep(cardinality = cardinality, recipe = recipe), )
		return cls(path)

	@staticmethod
	def _calc_src_dest(path):
		items = Items()
		for step in path:
			for (item, item_cardinality) in step.recipe.src.items():
				items.add(-step.cardinality * item_cardinality, item)
			for (item, item_cardinality) in step.recipe.dest.items():
				items.add(step.cardinality * item_cardinality, item)
		return items.src_dest()

	@property
	def src(self):
		return self._src

	@property
	def dest(self):
		return self._dest

	def cmpkey(self):
		return ("recipe_path", self._path)

	def net_value_known(self, eco):
		return all(recipes.net_value_known(eco) for recipes in self._path)

	def net_value(self, eco):
		return self.sell_value(eco) - self.buy_cost(eco)

	def buy_cost(self, eco):
		return self._path[0].buy_cost(eco)

	def sell_value(self, eco):
		return self._path[-1].sell_value(eco)

	def dump(self, eco = None):
		print("%s => %s" % (self.src.pretty_str(), self.dest.pretty_str()))
		for step in self:
			if step.cardinality != 1:
				print("    %4s %s" % (step.cardinality, step.recipe))
			else:
				print("         %s" % (step.recipe))
		print()
#		if eco is not None:
#			buy_cost = self.buy_cost(eco)
#			buy_str = ", ".join("%d x %s (%d)" %  (amount, buy_item.name, amount * eco.buy(buy_item)) for (buy_item, amount) in sorted(self._path[0].src.items()))
#			print("Buy for %d: %s" % (buy_cost, buy_str))
#		for recipe in self._path:
#			print(recipe)
#		if eco is not None:
#			sell_value = self.sell_value(eco)
#			sell_str = ", ".join("%d x %s (%d)" %  (amount, sell_item.name, amount * eco.sell(sell_item)) for (sell_item, amount) in sorted(self._path[-1].dest.items()))
#			print("Sell for %d: %s" % (sell_value, sell_str))

	def __iter__(self):
		return iter(self._path)

	def apply_substitution_recipes(self, recipes):
		new_path = list(self._path)
		for recipe in recipes:
			path_requires = self.src[recipe.dest.item]
			recipe_produces = recipe.dest[recipe.dest.item]
			scale_factor = fractions.Fraction(path_requires, recipe_produces)
			new_path.insert(0, self._PathStep(cardinality = scale_factor, recipe = recipe))
		return RecipePath(new_path)

	def substitutions(self, recipe_db):
		yield self

		possible_substitution_recipes = [ ]
		for item in self.src:
			substitution_recipes = recipe_db.recipes_that_produce(item)
			if len(substitution_recipes) > 0:
				substitution_recipes.append(None)
				possible_substitution_recipes.append(substitution_recipes)

		for selected_substitution_recipes in itertools.product(*possible_substitution_recipes):
			if all(recipe is None for recipe in selected_substitution_recipes):
				continue
			yield self.apply_substitution_recipes(selected_substitution_recipes)


