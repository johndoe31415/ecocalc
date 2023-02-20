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

class Resource():
	def __init__(self, identifier: str, name: str | None = None):
		self._identifier = identifier
		if name is None:
			self._name = identifier
		else:
			self._name = name

	@property
	def identifier(self):
		return self._identifier

	@property
	def name(self):
		return self._name

	@classmethod
	def from_dict(cls, identifier: str, serialized_obj: dict):
		return cls(identifier = identifier, name = serialized_obj.get("name"))

	def __repr__(self):
		return self.name
