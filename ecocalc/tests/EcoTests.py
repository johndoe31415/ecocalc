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
from ecocalc.ProductionSpecifier import ProductionSpecifier
from ecocalc.Enums import ComputationMode, RateUnit
from ecocalc.EconomyDefinition import EconomyDefinition
from ecocalc.RecipeResolver import RecipeResolver
from ecocalc.DisplayPreferences import DisplayPreferences

class EcoTests(unittest.TestCase):
	def setUp(self):
		self._eco = {
			"resources": {
				"a": { "name": "a" },
				"b": { "name": "b" },
				"c": { "name": "c" },
				"d": { "name": "d" },
				"e": { "name": "e" },
			},
			"production_entities": {
				"X": {
					"name": "X",
					"speed_factor": 0.75,
				},
				"Y": {
					"name": "Y",
					"speed_factor": 1.25,
				},
				"Z": {
					"name": "Z",
					"speed_factor": 10,
				},
			},
			"rate_scalars": {
				"yellow_belt":	{ "value": 15, "unit": "ups" },
				"red_belt":		{ "value": 1800, "unit": "upm" },
			},
			"recipes": [
				{ "recipe": "12 a + 7 b -> 13 c", "at": "X", "time": 9 },
			]
		}

	def test_full_belt_ups(self):
		eco = EconomyDefinition.load_from_dict(self._eco)
		production_specifier = ProductionSpecifier.parse(":yellow_belt c", eco)
		result = RecipeResolver(eco, computation_mode = ComputationMode.Rate, rate_unit = RateUnit.UnitsPerSecond).resolve([ production_specifier ])
		production = next(result.production)
		self.assertEqual(production.production_speed, fractions.Fraction(3, 4))
		self.assertEqual(production.cardinality, fractions.Fraction(180, 13))
		self.assertEqual(list(production.lhs), [ ("a", fractions.Fraction(180, 13)), ("b", fractions.Fraction(105, 13)) ])
		self.assertEqual(list(production.rhs), [ ("c", 15) ])
