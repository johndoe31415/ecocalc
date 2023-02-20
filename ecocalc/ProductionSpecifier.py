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
	def __init__(self, parsed_specifier):
		self._parsed_specifier = parsed_specifier
		if ("multiplier" in self._parsed_specifier) and ("rate_scalar" in self._parsed_specifier["multiplier"]) and (self._parsed_specifier["recipe"][0] == "recipe_no"):
			raise InvalidProductionSpecifierException(f"Having a rate scalar in a production specifier (here: {self._parsed_specifier['multiplier']['rate_scalar']}) only makes sense when defining an output product, not a recipe number (here: #{self._parsed_specifier['recipe'][1]}).")

	@classmethod
	def parse(cls, production_specifier_str: str):
		parsed_production_specifier = parse_production_specifier(production_specifier_str)
		_log.debug("Parsed production specifier: %s", parsed_production_specifier)
		return cls(parsed_production_specifier)
