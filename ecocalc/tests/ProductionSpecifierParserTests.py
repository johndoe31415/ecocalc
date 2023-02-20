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
from ecocalc.Parser import parse_production_specifier

class ProductionSpecifierParserTests(unittest.TestCase):
	def test_simple_1(self):
		self.assertEqual(parse_production_specifier("iron_plate"), {
			"recipe":	("recipe_id", "iron_plate"),
		})

	def test_simple_2(self):
		self.assertEqual(parse_production_specifier("#123"), {
			"recipe":	("recipe_no", 123),
		})

	def test_multiplier_1(self):
		self.assertEqual(parse_production_specifier("1.234 iron_plate"), {
			"recipe":	("recipe_id", "iron_plate"),
			"multiplier":	fractions.Fraction("1.234"),
		})

	def test_multiplier_2(self):
		self.assertEqual(parse_production_specifier("14 #123"), {
			"recipe":		("recipe_no", 123),
			"multiplier":	14,
		})

	def test_multiplier_at_1(self):
		self.assertEqual(parse_production_specifier("14 #123 @constructor"), {
			"recipe":		("recipe_no", 123),
			"multiplier":	14,
			"at":			"constructor",
		})

	def test_multiplier_at_2(self):
		self.assertEqual(parse_production_specifier("14 #123 @constructor"), {
			"recipe":		("recipe_no", 123),
			"multiplier":	14,
			"at":			"constructor",
		})

	def test_multiplier_at_speed_1(self):
		self.assertEqual(parse_production_specifier("14 #123 @constructor 1.25"), {
			"recipe":		("recipe_no", 123),
			"multiplier":	14,
			"at":			"constructor",
			"speed":		fractions.Fraction("1.25"),
		})

	def test_multiplier_at_speed_2(self):
		self.assertEqual(parse_production_specifier("14 #123 @constructor 250%"), {
			"recipe":		("recipe_no", 123),
			"multiplier":	14,
			"at":			"constructor",
			"speed":		fractions.Fraction(250, 100),
		})
