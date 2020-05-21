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

from Comparable import Comparable

class Item(Comparable):
	def __init__(self, name):
		Comparable.__init__(self)
		self._name = name

	def cmpkey(self):
		return ("item", self.name.lower())

	@property
	def name(self):
		return self._name

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "<%s>" % (self.name)

class Items(object):
	def __init__(self):
		self._counts = { }
		self._frozen = False

	def src_dest(self):
		src = Items()
		dest = Items()
		for (item, cardinality) in self.items():
			if cardinality < 0:
				src.add(-cardinality, item)
			else:
				dest.add(cardinality, item)
		src.freeze()
		dest.freeze()
		return (src, dest)

	def freeze(self):
		self._frozen = True

	@property
	def item(self):
		assert(len(self) == 1)
		for item in self._counts:
			return item

	def pretty_str(self):
		return " + ".join("%s %s" % (count, item.name) for (item, count) in sorted(self._counts.items()))

	def add(self, cardinality, item):
		assert(isinstance(item, Item))
		assert(not self._frozen)
		self._counts[item] = self[item] + cardinality
		if self._counts[item] == 0:
			del self._counts[item]

	def add_all(self, cardinality, items):
		for (item, item_cardinality) in items.items():
			self.add(cardinality * item_cardinality, item)

	def dump(self):
		for (item, count) in sorted(self._counts.items()):
			print("%4s %s" % (count, item.name))
		print()

	def __getitem__(self, key):
		return self._counts.get(key, 0)

	def items(self):
		return self._counts.items()

	def __iter__(self):
		return iter(self._counts)

	def __len__(self):
		return len(self._counts)

	def __str__(self):
		return "Items<%s>" % (self.pretty_str())

