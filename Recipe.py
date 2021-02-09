#	ecocalc - The X.509 Swiss Army Knife white-hat certificate toolkit
#	Copyright (C) 2017-2021 Johannes Bauer
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
import collections
from Tools import NumberTools

Resource = collections.namedtuple("Resource", [ "name", "count" ])

class Recipe():
	FINISHED = "__finished__"
	_RECIPE_RE = re.compile("(?P<lhs>.*)->(?P<rhs>.*)")
	_ITEM_RE = re.compile("(?P<cardinality>\d+)?\s*(?P<name>[-a-zA-Z0-9_]+)")

	def __init__(self, input_tuple, output_tuple, scalar = 1, name = None, produced_at = None, is_rate = False):
		self._in = input_tuple
		self._out = output_tuple
		self._scalar = scalar
		self._name = name
		self._produced_at = produced_at
		self._is_rate = is_rate

	@property
	def is_rate(self):
		return self._is_rate

	@property
	def scalar(self):
		return self._scalar

	@property
	def name(self):
		return self._name

	@property
	def produced_at(self):
		return self._produced_at

	@classmethod
	def empty_recipe(cls, name = None, is_rate = False):
		return cls(input_tuple = tuple(), output_tuple = tuple(), name = name, is_rate = is_rate)

	@property
	def ingredients(self):
		return iter(self._in)

	@property
	def products(self):
		return iter(self._out)

	@classmethod
	def from_inout_tuple(cls, inout_tuple, scalar = 1, name = None, is_rate = False):
		lhs = [ ]
		rhs = [ ]
		for item in inout_tuple:
			if item.count == 0:
				pass
			elif item.count < 0:
				lhs.append(Resource(name = item.name, count = -item.count))
			else:
				rhs.append(Resource(name = item.name, count = item.count))
		return cls(tuple(lhs), tuple(rhs), scalar = scalar, name = name, is_rate = is_rate)

	@staticmethod
	def _scaled_tuple(item_tuple, scalar):
		for item in item_tuple:
			yield Resource(name = item.name, count = scalar * item.count)

	@property
	def scaled_input_tuple(self):
		return self._scaled_tuple(self._in, self.scalar)

	@property
	def scaled_output_tuple(self):
		return self._scaled_tuple(self._out, self.scalar)

	@property
	def resources(self):
		resources = set()
		resources |= set(item.name for item in self._in)
		resources |= set(item.name for item in self._out)
		return resources

	@property
	def scaled_inout_tuple(self):
		return self._add_sides(self._scaled_tuple(self._in, -self.scalar), self._scaled_tuple(self._out, self.scalar))

	def _format_side(self, item_tuple, economy = None):
		formatted_items = [ ]
		for item in item_tuple:
			if item.name == Recipe.FINISHED:
				formatted_items.append("Finished")
				continue

			pretty_name = item.name if (economy is None) else economy.get_resource_name(item.name)
			if not self.is_rate:
				if item.count == 1:
					text = "%s" % (pretty_name)
				else:
					text = "%s %s" % (NumberTools.num2str(item.count), pretty_name)
			else:
				text = "%s/min %s" % (NumberTools.num2str(item.count), pretty_name)
			formatted_items.append(text)
		return " + ".join(formatted_items)

	def pretty_string(self, economy, show_scaled = False, show_rate = False):
		prefix_list = [ value for value in [ self.name, self.produced_at ] if (value is not None) ]
		if len(prefix_list) == 0:
			prefix = ""
		else:
			prefix = "{%s}" % (" / ".join(prefix_list))

		if show_scaled or (self.scalar == 1):
			(lhs, rhs) = (self.scaled_input_tuple, self.scaled_output_tuple)
		else:
			(lhs, rhs) = (self._in, self._out)
		lhs = self._format_side(lhs, economy = economy)
		rhs = self._format_side(rhs, economy = economy)

		if show_scaled:
			return "%s %s →  %s" % (prefix, lhs, rhs)
		else:
			return "%s x %s [ %s →  %s ]" % (NumberTools.num2str(self.scalar), prefix, lhs, rhs)

	@classmethod
	def _parse_recipe_side(cls, side_str, cycle_time = None):
		side = [ ]
		for item in side_str.split("+"):
			item = item.strip()
			match = cls._ITEM_RE.fullmatch(item)
			if match is None:
				raise Exception("Not a valid item descriptor: %s" % (item))
			match = match.groupdict()
			if match["cardinality"] is None:
				match["cardinality"] = 1
			else:
				match["cardinality"] = int(match["cardinality"])

			if cycle_time is None:
				# Cardinalities only
				count = match["cardinality"]
			else:
				# Rates recipe
				count = match["cardinality"] / cycle_time * 60
			side.append(Resource(name = match["name"], count = count))
		return tuple(side)

	@classmethod
	def from_str(cls, recipe_str, name = None, produced_at = None, cycle_time = None):
		match = cls._RECIPE_RE.fullmatch(recipe_str)
		if match is None:
			raise Exception("Not a valid recipe string: %s" % (recipe_str))
		match = match.groupdict()
		input_tuple = cls._parse_recipe_side(match["lhs"], cycle_time = cycle_time)
		output_tuple = cls._parse_recipe_side(match["rhs"], cycle_time = cycle_time)
		return cls(input_tuple, output_tuple, name = name, produced_at = produced_at, is_rate = cycle_time is not None)

	@staticmethod
	def _add_sides(*sides):
		total_sum = collections.OrderedDict()
		for side in sides:
			for item in side:
				if item.name in total_sum:
					total_sum[item.name] += item.count
				else:
					total_sum[item.name] = item.count
		recipe_sum = tuple(Resource(name = item_name, count = sum_value) for (item_name, sum_value) in total_sum.items())
		return recipe_sum

	def __add__(self, other):
		assert(self.is_rate == other.is_rate)
		sum_recipe = self._add_sides(self.scaled_inout_tuple, other.scaled_inout_tuple)
		return Recipe.from_inout_tuple(sum_recipe, is_rate = self.is_rate)

	def __mul__(self, scalar):
		return Recipe(self._in, self._out, name = self.name, produced_at = self.produced_at, scalar = self.scalar * scalar, is_rate = self.is_rate)

	def __repr__(self):
		return "<%s>" % (str(self))

	def __str__(self):
		lhs = self._format_side(self.scaled_input_tuple)
		rhs = self._format_side(self.scaled_output_tuple)
		return "%s →  %s" % (lhs, rhs)
