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

from .Enums import ComputationMode, RateUnit
from .Production import Production
from .RecipeSum import RecipeSum
from .Exceptions import UnknownResourceException, UnknownProductionEntityException

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
#			if recipe.rhs.resource_count != 1:
#				continue
			if (self._computation_mode == ComputationMode.Rate) and (not recipe.provides_rate):
				continue
			yield recipe

	def _find_production_entity(self, production_entity_or_entity_group):
		if self._economy.has_production_entity_group(production_entity_or_entity_group):
			group = self._economy.get_production_entity_group(production_entity_or_entity_group)
			return self._find_production_entity(group.members[0])

		if self._economy.has_production_entity(production_entity_or_entity_group):
			entity = self._economy.get_production_entity(production_entity_or_entity_group)
			return entity

		raise UnknownProductionEntityException(f"No such production entity: {production_entity_or_entity_group}")

	def get_recipe_which_produces(self, resource):
		for recipe in self._recipes:
			if recipe.produces(resource):
				return recipe

	def produce_resource(self, resource, target_rate_or_count):
		# Find the recipe first that produces what we want
		recipe = self.get_recipe_which_produces(resource)

		if recipe is None:
			return None

		# Figure out where we will produce it
		production_entity = self._find_production_entity(recipe.at)

		# Compute the cardinality of production units we need to achieve the
		# deired target rate/count
		unity_value = recipe.rhs[resource]
		if self._computation_mode == ComputationMode.Rate:
			unity_value /= recipe.execution_time_secs
			speed_factor = production_entity.max_speed_factor
			unity_value *= speed_factor
			if self._rate_unit == RateUnit.UnitsPerMinute:
				target_rate_or_count_per_sec = target_rate_or_count / 60
			else:
				target_rate_or_count_per_sec = target_rate_or_count
		else:
			speed_factor = None

		cardinality = target_rate_or_count_per_sec / unity_value
		production = Production(recipe, production_entity, speed_factor, cardinality)
		return production

	def produce_production_specifier(self, production_specifier):
		if production_specifier.references_resource:
			if not self._economy.has_resource(production_specifier.referenced_resource):
				raise UnknownResourceException(f"Unknown resource, do not know how to produce: {production_specifier.referenced_resource}")
			return self.produce_resource(production_specifier.referenced_resource, production_specifier.target_rate_or_count)
		else:
			raise NotImplementedError()

	def _recursively_resolve(self, production, recipe_sum):
		for (required_resource_id, required_rate_or_count) in production.lhs:
			production = self.produce_resource(required_resource_id, required_rate_or_count)
			if production is not None:
				recipe_sum += production
				self._recursively_resolve(production, recipe_sum)

	def resolve(self, production_specifiers):
		recipe_sum = RecipeSum()
		for production_specifier in production_specifiers:
			production = self.produce_production_specifier(production_specifier)
			recipe_sum += production
			self._recursively_resolve(production, recipe_sum)
		recipe_sum.merge_recipes()
		return recipe_sum
