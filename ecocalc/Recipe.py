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
import functools
import collections
import fractions
from .Parser import parse_recipe

_log = logging.getLogger(__spec__.name)

class RecipeSide():
	def __init__(self, resources):
		self._resources = resources
		self._economy = None
		self._resourcedict = collections.defaultdict(int)
		for (cardinality, resource) in self._resources:
			self._resourcedict[resource] += cardinality

	@property
	def economy(self):
		return self._economy

	@economy.setter
	def economy(self, value):
		self._economy = value

	@functools.cached_property
	def ingredients(self):
		return set(self._resourcedict)

	@property
	def resource_count(self):
		return len(self._resourcedict)

	def contains(self, resource_id):
		return resource_id in self._resourcedict

	def __getitem__(self, resource_id):
		return self._resourcedict[resource_id]

	def __format__(self, fmtspec):
		if self.economy is None:
			return " + ".join(f"{cardinality:{fmtspec}} {resource}" for (cardinality, resource) in self._resources)
		else:
			return " + ".join(f"{cardinality:{fmtspec}} {self.economy.get_resource_name(resource)}" for (cardinality, resource) in self._resources)

	def __repr__(self):
		return format(self)

class Recipe():
	def __init__(self, lhs: RecipeSide, rhs: RecipeSide, at: str, execution_time_secs: fractions.Fraction | None = None, name: str | None = None):
		self._lhs = lhs
		self._rhs = rhs
		self._at = at
		self._execution_time_secs = execution_time_secs
		self._name = name
		self._economy = None

	@property
	def economy(self):
		return self._economy

	@economy.setter
	def economy(self, value):
		self._economy = value
		self._lhs.economy = value
		self._rhs.economy = value

	@functools.cached_property
	def ingredients(self):
		ingredients = set()
		ingredients |= self.lhs.ingredients
		ingredients |= self.rhs.ingredients
		return ingredients

	@functools.cached_property
	def is_cyclic(self):
		return len(self.lhs.ingredients & self.rhs.ingredients) > 0

	@property
	def lhs(self):
		return self._lhs

	@property
	def rhs(self):
		return self._rhs

	@property
	def at(self):
		return self._at

	@property
	def execution_time_secs(self):
		return self._execution_time_secs

	@property
	def name(self):
		return self._name

	@property
	def provides_rate(self):
		return self.execution_time_secs is not None

	def produces(self, resource_id):
		return self.rhs.contains(resource_id)

	@classmethod
	def _parse_recipe_equation(cls, recipe_str):
		(lhs, rhs) = parse_recipe(recipe_str)
		_log.debug("Parsed recipe: %s -> %s", lhs, rhs)
		lhs = RecipeSide(lhs)
		rhs = RecipeSide(rhs)
		return (lhs, rhs)

	@classmethod
	def from_dict(cls, serialized_obj: dict):
		(lhs, rhs) = cls._parse_recipe_equation(serialized_obj["recipe"])
		kwargs = {
			"lhs":					lhs,
			"rhs":					rhs,
			"at":					serialized_obj["at"],
			"execution_time_secs":	serialized_obj.get("time"),
			"name":					serialized_obj.get("name"),
		}
		return cls(**kwargs)

	def __format__(self, fmtspec):
		return f"{self.lhs:{fmtspec}} -> {self.rhs:{fmtspec}}"

	def __repr__(self):
		return format(self)
