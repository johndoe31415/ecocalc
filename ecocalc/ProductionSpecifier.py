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

import re
import logging
from .Parser import parse_production_specifier
from .Exceptions import InvalidProductionSpecifierException

_log = logging.getLogger(__spec__.name)

class ProductionSpecifier():
	def __init__(self, parsed_specifier, economy = None):
		self._parsed_specifier = parsed_specifier
		if ("multiplier" in self._parsed_specifier) and ("rate_scalar" in self._parsed_specifier["multiplier"]) and self.references_recipe:
			raise InvalidProductionSpecifierException(f"Having a rate scalar in a production specifier (here: {self._parsed_specifier['multiplier']['rate_scalar']}) only makes sense when defining an output product, not a recipe number (here: #{self._parsed_specifier['recipe'][1]}).")
		self._economy = economy

	@classmethod
	def parse(cls, production_specifier_str: str, economy = None):
		parsed_production_specifier = parse_production_specifier(production_specifier_str)
		_log.debug("Parsed production specifier: %s", parsed_production_specifier)
		return cls(parsed_production_specifier, economy = economy)

	@property
	def target_rate_or_count(self):
		value = 1
		if "multiplier" in self._parsed_specifier:
			if "value" in self._parsed_specifier["multiplier"]:
				value *= self._parsed_specifier["multiplier"]["value"]
			if "rate_scalar" in self._parsed_specifier["multiplier"]:
				value *= self._economy.get_rate_scalar(self._parsed_specifier["multiplier"]["rate_scalar"]).scalar_upm
		return value

	@property
	def references_recipe(self):
		return self._parsed_specifier["recipe"][0] == "recipe_no"

	@property
	def references_item(self):
		return not self.references_recipe

	@property
	def referenced_item(self):
		return self._parsed_specifier["recipe"][1]

	def __repr__(self):
		return str(self._parsed_specifier)
