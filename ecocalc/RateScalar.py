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

class RateScalar():
	def __init__(self, scalar_upm: float):
		scalar_upm = scalar_upm

	@property
	def scalar_upm(self):
		return self._scalar_upm

	@classmethod
	def from_dict(cls, serialized_obj: dict):
		if serialized_obj["unit"] == "upm":
			return cls(scalar_upm = serialized_obj["value"])
		elif serialized_obj["unit"] == "ups":
			return cls(scalar_upm = 60 * serialized_obj["value"])
		else:
			raise NotImplementedError(serialized_obj["unit"])

	def __repr__(self):
		return f"{self.upm}/min"
