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

import re

class Resource():
	_NAME_TO_ID_RE = re.compile("[^a-zA-Z0-9]")
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
	def _name_to_identifier(cls, name):
		return cls._NAME_TO_ID_RE.sub("_", name).lower()

	@classmethod
	def from_dict(cls, name: str, serialized_obj: dict):
		if "id" in serialized_obj:
			identifier = serialized_obj["id"]
		else:
			identifier = cls._name_to_identifier(name)
		return cls(identifier = identifier, name = name)

	def __repr__(self):
		return f"Res<{self.name}>"
