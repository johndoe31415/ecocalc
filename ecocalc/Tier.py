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

_log = logging.getLogger(__spec__.name)

class Tier():
	def __init__(self, enabled_tags):
		self._enabled_tags = enabled_tags
		self._economy = None

	@property
	def enabled_tags(self):
		return self._enabled_tags

	@property
	def economy(self):
		return self._economy

	@economy.setter
	def economy(self, value):
		self._economy = value

	@classmethod
	def from_dict(cls, serialized_obj: str):
		enabled_tags = set(tag.strip() for tag in serialized_obj.split("+"))
		return cls(enabled_tags = enabled_tags)
