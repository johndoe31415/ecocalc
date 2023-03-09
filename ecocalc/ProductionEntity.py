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

import fractions

class ProductionEntity():
	def __init__(self, identifier: str, name: str | None = None, min_speed_factor: fractions.Fraction = 1, max_speed_factor: fractions.Fraction = 1, tag: str | None = None):
		self._identifier = identifier
		if name is None:
			self._name = identifier
		else:
			self._name = name
		self._min_speed_factor = min_speed_factor
		self._max_speed_factor = max_speed_factor
		self._tag = tag

	@property
	def identifier(self):
		return self._identifier

	@property
	def name(self):
		return self._name

	@property
	def min_speed_factor(self):
		return self._min_speed_factor

	@property
	def max_speed_factor(self):
		return self._max_speed_factor

	@property
	def single_speed(self):
		return self.min_speed_factor == self.max_speed_factor

	@property
	def tag(self):
		return self._tag

	@classmethod
	def from_dict(cls, identifier: str, serialized_obj: dict):
		kwargs = {
			"identifier":	identifier,
			"name":			serialized_obj["name"],
			"tag":			serialized_obj.get("tag"),
		}
		if "speed_factor" in serialized_obj:
			kwargs.update({
				"min_speed_factor":		fractions.Fraction(serialized_obj["speed_factor"]),
				"max_speed_factor":		fractions.Fraction(serialized_obj["speed_factor"]),
			})
		elif ("min_speed_factor" in serialized_obj) and ("max_speed_factor" in serialized_obj):
			kwargs.update({
				"min_speed_factor":		fractions.Fraction(serialized_obj["min_speed_factor"]),
				"max_speed_factor":		fractions.Fraction(serialized_obj["max_speed_factor"]),
			})
		return cls(**kwargs)

	def __repr__(self):
		if self.min_speed_factor == self.max_speed_factor:
			return f"{self.name} ({float(self.min_speed_factor * 100):.0f}%)"
		else:
			return f"{self.name} ({float(self.min_speed_factor * 100):.0f}-{float(self.max_speed_factor * 100):.0f}%)"
