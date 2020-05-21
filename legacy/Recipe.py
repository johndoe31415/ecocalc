#	ecocalc - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2017-2020 Johannes Bauer
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
from Items import Items, Item
from Comparable import Comparable
from Exceptions import ParseError

class Recipe(Comparable):
	_RECIPE_LINE_RE = re.compile(r"(?P<lhs>[^-]+)-(\((?P<via>.*)\))?-*>(?P<rhs>.*)")

	def __init__(self, src_items, dst_items, via = None, path = None):
		assert(len(dst_items) == 1)
		self._source = src_items
		self._dest = dst_items
		self._via = via
		if path is None:
			self._path = [ ]
		else:
			self._path = path

	def cmpkey(self):
		return ("recipe", self._source, self._dest)

	@property
	def src(self):
		return self._source

	@property
	def dest(self):
		return self._dest

#	def substitute(self, recipe):
#		if recipe.dest.item not in self.src:
#			raise Exception("%s cannot be subsituted in %s, because %s is not a source ingredient of %s." % (recipe, self, recipe.dest.item, self))
#
#		clone = self.clone()
#		clone._path.append(recipe)
#
#		dest_cardinality = recipe.dest[recipe.dest.item]
#		src_cardinality = self.src[recipe.dest.item]
#		scalar = fractions.Fraction(src_cardinality, dest_cardinality)
#
#		for (item, cardinality) in recipe.src.items():
#			clone.src.add(cardinality * scalar, item)
#		for (item, cardinality) in recipe.dest.items():
#			clone.src.add(-cardinality * scalar, item)
#		return clone

	@classmethod
	def _parse_side(cls, side):
		items = Items()
		for item in side.split("+"):
			item = item.strip()
			item = item.split(" ", maxsplit = 1)
			cardinality = int(item[0])
			name = item[1]
			items.add(cardinality, Item(name))
		return items

	@classmethod
	def parse_line(cls, line):
		result = cls._RECIPE_LINE_RE.fullmatch(line)
		if result is None:
			raise ParseError("lefthand/righthand side could not be parsed.")
		result = result.groupdict()
		lhs = cls._parse_side(result["lhs"])
		rhs = cls._parse_side(result["rhs"])
		via = result["via"]
		return cls(lhs, rhs, via)

	def __repr__(self):
		return "\"%s\"" % (str(self))

	def __str__(self):
		if self._via is None:
			return "%s --> %s" % (self._source.pretty_str(), self._dest.pretty_str())
		else:
			return "%s --(%s)--> %s" % (self._source.pretty_str(), self._via, self._dest.pretty_str())

