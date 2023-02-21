#	ecocalc - Economy calculation for factory-building games
#	Copyright (C) 2020-2023 Johannes Bauer
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

from .Enums import ComputationMode

class RecipeResolver():
	def __init__(self, economy, computation_mode, rate_unit):
		self._economy = economy
		self._computation_mode = computation_mode
		self._rate_unit = rate_unit
		self._recipes = list(self._filter_recipes())

	def _filter_recipes(self):
		for recipe in self._economy.recipes:
			if recipe.is_cyclic:
				continue
#			if recipe.rhs.item_count != 1:
#				continue
			if (self._computation_mode == ComputationMode.Rate) and (not recipe.provides_rate):
				continue
			yield recipe

	def get_recipe_which_produces(self, item):
		pass

	def produce_item(self, item, target_rate_or_count):
		pass

	def produce_production_specifier(self, production_specifier):
		if production_specifier.references_item:
			print(production_specifier)
			print(production_specifier.target_rate_or_count)
		else:
			raise NotImplementedError()

	def resolve(self, production_specifiers):
		for production_specifier in production_specifiers:
			production = self.produce_production_specifier(production_specifier)
