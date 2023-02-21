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

from .tpg import tpg
import fractions

class EcoCalcParser(tpg.Parser):
	r"""
		set lexer = ContextSensitiveLexer

		separator space '\s+';

		token identifier	'[a-zA-Z_][-a-zA-Z_0-9]*';
		token float			'(\d*)?\.(\d+)';
		token integer		'\d+';
		token percent		'%';
		token recipe_no		'#';
		token at_facility	'@';

		ProductionSpecifier/lhs ->							$ lhs = { }
			(
				MultiplierValue/m							$ lhs["multiplier"] = m
			)?
			RecipeSpecifier/r								$ lhs["recipe"] = r
			(
				At/a										$ lhs["at"] = a
			)?
			(
				Value/s										$ lhs["speed"] = s
			)?
		;

		RecipeSpecifier/lhs -> (
				recipe_no integer/i							$ lhs = ("recipe_no", int(i))
				| identifier/n								$ lhs = ("recipe_id", n)
		);

		Recipe/lhs ->
			RecipeSide/left '->' RecipeSide/right			$ lhs = (left, right)
		;

		RecipeSide/lhs ->									$ lhs = [ ]
			RecipeElement/e									$ lhs.append(e)
			(
				'\+' RecipeElement/e						$ lhs.append(e)
			)*
		;

		RecipeElement/lhs ->								$ v = 1
			(
				Value/v
			)?
			identifier/n									$ lhs = (v, n)
		;

		MultiplierValue/lhs -> (
				Value/v ':' identifier/n					$ lhs = { "value": v, "rate_scalar": n }
				| ':' identifier/n							$ lhs = { "rate_scalar": n }
				| Value/v									$ lhs = { "value": v }
		);

		Value/lhs -> (
				Atom/n '/' Atom/d							$ lhs = fractions.Fraction(n, d)
				| Atom/v percent							$ lhs = fractions.Fraction(v, 100)
				| Atom/lhs
		);

		Atom/lhs -> (
				float/f										$ lhs = fractions.Fraction(f)
				| integer/i									$ lhs = int(i)
		);

		At/lhs -> at_facility identifier/lhs;
	"""

def parse_production_specifier(expr):
	parser = EcoCalcParser()
	return parser.parse("ProductionSpecifier", expr)

def parse_recipe(expr):
	parser = EcoCalcParser()
	return parser.parse("Recipe", expr)

if __name__ == "__main__":
	import sys

	testcases = sys.argv[1:]
	for input_value in testcases:
		try:
			#parsed = parse_production_specifier(input_value)
			parsed = parse_recipe(input_value)
			print(parsed)
		except Exception as e:
			print(tpg.exc())
			raise
