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
import collections

_log = logging.getLogger(__spec__.name)

class RecipeSum():
	def __init__(self):
		self._production = [ ]

	@property
	def production(self):
		return iter(self._production)

	def print(self, display_preferences):
		for production in self._production:
			print(production.format(display_preferences))

	def merge_recipes(self):
		merged_production = collections.OrderedDict()
		for production in self._production:
			if production.recipe not in merged_production:
				merged_production[production.recipe] = production
			else:
				merged_production[production.recipe] = merged_production[production.recipe] + production
		self._production = list(merged_production.values())

	def __iadd__(self, production):
		self._production.append(production)
		return self

	def __imul__(self, scalar):
		self._production = [ production * scalar for production in self._production ]
		return self
