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

_log = logging.getLogger(__spec__.name)

class Production():
	def __init__(self, recipe, production_entity, cardinality):
		self._recipe = recipe
		self._production_entity = production_entity
		self._production_speed = production_entity.max_speed_factor
		self._cardinality = cardinality

	@property
	def recipe(self):
		return self._recipe

	@property
	def production_entity(self):
		return self._production_entity

	@property
	def production_speed(self):
		return self._production_speed

	@property
	def cardinality(self):
		return self._cardinality

	def __mul__(self, scalar):
		return Production(self.recipe, self.production_entity, self.cardinality * scalar)

	def __repr__(self):
		return "{self.cardinality} x {self.recipe} @ {self.production_entity} / {self.production_speed}"
