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

class ProductionSpecifier():
	"""
	Specifies a production specifier. Can be in different formats, e.g.:

	Format 1:
	   [number] (rate_scalar)? [resource_name]
	Examples:
	   400 copper_plate
	   1800/2 copper_plate
	   1.234 copper_plate
	   1 blue_belt iron_plate


	Format 2:
		#[recipe_number/name] (@production_facility)? (xspeed(%)?)?
	Examples:
		#4
		#mk_iron_plt
		#12 @assembler_mk3
		#12 @constructor x1.25
		#12 @constructor x250%
	"""

	@classmethod
	def parse(cls, production_specifier_str: str):
		production_specifier_str = production_specifier_str.strip(" \t\r\n")


