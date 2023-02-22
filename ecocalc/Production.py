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

import logging
import fractions
import math
from .DisplayPreferences import EntityCardinalityFormat, DisplayPreferences

_log = logging.getLogger(__spec__.name)

class Production():
	def __init__(self, recipe, production_entity, production_speed, cardinality):
		assert(isinstance(cardinality, fractions.Fraction))
		self._recipe = recipe
		self._production_entity = production_entity
		self._production_speed = production_speed
		self._cardinality = cardinality

	@property
	def recipe(self):
		return self._recipe

	@property
	def production_entity(self):
		return self._production_entity

	@property
	def production_speed(self):
		"""Speed at which production facilities are set to (e.g., assembler
		coefficient or overclocking speed)."""
		return self._production_speed

	@property
	def cardinality(self):
		"""Number of production facilities (e.g., assemblers)."""
		return self._cardinality

	@property
	def total_scalar(self):
		return self.cardinality * self.production_speed

	@property
	def lhs(self):
		for (resource_id, cardinality) in self.recipe.lhs.resource_dict.items():
			yield (cardinality * self.total_scalar / self.recipe.execution_time_secs, resource_id)

	@property
	def rhs(self):
		for (resource_id, cardinality) in self.recipe.rhs.resource_dict.items():
			yield (cardinality * self.total_scalar / self.recipe.execution_time_secs, resource_id)

	def __mul__(self, scalar):
		return Production(self.recipe, self.production_entity, self.production_speed, self.cardinality * scalar)

	def __add__(self, other):
		assert(self.recipe == other.recipe)
		assert(self.production_entity == other.production_entity)
		assert(self.production_speed == other.production_speed)
		return Production(self.recipe, self.production_entity, self.production_speed, self.cardinality + other.cardinality)

	def _format_cardinality(self, display_preferences):
		match display_preferences.entity_cardinality_format:
			case EntityCardinalityFormat.RoundedCeiling:
				return str(math.ceil(self.cardinality))

			case EntityCardinalityFormat.FloatingPoint:
				return f"{float(self.cardinality):.2f}"

			case EntityCardinalityFormat.Fractional:
				return str(self.cardinality)
		raise NotImplementedError()

	def format(self, display_preferences):
		cardinality = self._format_cardinality(display_preferences)
		production_entity = str(self.production_entity)
		recipe = self.recipe.format(display_preferences, multiplier = self.total_scalar / self.recipe.execution_time_secs)
		if self.production_entity.single_speed:
			return f"{cardinality} x {production_entity}: {recipe}"
		else:
			return f"{cardinality} x {production_entity} @ {self.production_speed * 100:.0f}%: {recipe}"

	def __repr__(self):
		display_preferences = DisplayPreferences()
		return self.format(display_preferences)
