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

class ProductionEntityGroup():
	def __init__(self, identifier: str, members: list[str]):
		self._identifier = identifier
		self._members = members

	@property
	def identifier(self):
		return self._identifier

	@property
	def members(self):
		return self._members

	@classmethod
	def from_list(cls, identifier: str, serialized_obj: list):
		kwargs = {
			"identifier":	identifier,
			"members":		serialized_obj,
		}
		return cls(**kwargs)

	def __repr__(self):
		return f"{self.identifier} ({len(self.members)} aliases)"
