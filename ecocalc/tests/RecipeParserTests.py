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

import unittest
import fractions
from ecocalc.Parser import parse_recipe

class RecipeParserTests(unittest.TestCase):
	def test_simple_1(self):
		self.assertEqual(parse_recipe("iron -> plate"),
		(
			[ (1, "iron") ],
			[ (1, "plate") ],
		))

	def test_simple_2(self):
		self.assertEqual(parse_recipe("iron + foo -> plate"),
		(
			[ (1, "iron"), (1, "foo") ],
			[ (1, "plate") ],
		))

	def test_simple_3(self):
		self.assertEqual(parse_recipe("12 iron + 34 foo -> 9 plate + 2 bar"),
		(
			[ (12, "iron"), (34, "foo") ],
			[ (9, "plate"), (2, "bar") ],
		))

