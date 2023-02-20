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

class RecipeSide():
	def __init__(self):
		pass

	@classmethod
	def parse(cls, side_str):
		return cls()

	def __repr__(self):
		pass

class Recipe():
	def __init__(self, lhs: RecipeSide, rhs: RecipeSide, at: str, execution_time: float | None = None, name: str | None = None):
		self._lhs = lhs
		self._rhs = rhs
		self._at = at
		self._execution_time = execution_time
		self._name = name

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
	def execution_time(self):
		return self._execution_time

	@property
	def name(self):
		return self._name

	@classmethod
	def _parse_recipe_equation(cls, recipe_str):
		(lhs_str, rhs_str) = recipe_str.split("->")
		lhs = RecipeSide.parse(lhs_str)
		rhs = RecipeSide.parse(rhs_str)
		return (lhs, rhs)

	@classmethod
	def from_dict(cls, serialized_obj: dict):
		(lhs, rhs) = cls._parse_recipe_equation(serialized_obj["recipe"])
		kwargs = {
			"lhs":				lhs,
			"rhs":				rhs,
			"at":				serialized_obj["at"],
			"execution_time":	serialized_obj.get("time"),
			"name":				serialized_obj.get("name"),
		}
		return cls(**kwargs)

	def __repr__(self):
		return f"{self.lhs} -> {self.rhs}"