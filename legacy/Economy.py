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

import re
from Items import Item

class Economy(object):
	_ECO_RE = re.compile(r"(?P<item>[^(=]+)(\((?P<item_id>[^)]+)\))?\s*=\s*(?P<value>\d+)\s*")
	def __init__(self, buy_scalar, sell_scalar):
		self._buy_scalar = buy_scalar
		self._sell_scalar = sell_scalar
		self._values = { }

	@classmethod
	def create_factors_from_skill(cls, skill_level, haggling_percent = 0, allure_percent = 0, fortify_barter_percent = 0):
		assert(0 <= skill_level <= 100)
		(barter_min, barter_max) = (2.0, 3.3)
		base_factor = ((barter_max * (100 - skill_level)) + (barter_min * skill_level)) / 100
		modifier = (1 + (haggling_percent / 100)) * (1 + (allure_percent / 100)) * (1 + (fortify_barter_percent / 100))
		buy_scalar = base_factor / modifier
		sell_scalar = base_factor * modifier
		if sell_scalar < 1:
			sell_scalar = 1
		if buy_scalar < 1.05:
			buy_scalar = 1.05
		return cls(buy_scalar = buy_scalar, sell_scalar = sell_scalar)

	def add(self, item, item_id, value):
		self._values[item] = value

	def known(self, item):
		return item in self._values

	def buy(self, item):
		return round(self._values[item] * self._buy_scalar)

	def sell(self, item):
		return round(self._values[item] / self._sell_scalar)

	def total_price_cost(self, recipe):
		buy_cost = 0
		sell_price = 0
		for (item, count) in recipe.src.items():
			buy_cost += count * self.buy(item)
		for (item, count) in recipe.dest.items():
			sell_price += count * self.sell(item)
		return (buy_cost, sell_price)

	def net_value(self, recipe):
		(buy_cost, sell_price) = self.total_price_cost(recipe)
		return sell_price - buy_cost

	@classmethod
	def _parse_line(cls, line):
		result = cls._ECO_RE.fullmatch(line)
		if result is None:
			raise Exception("Syntax error in economy line.")

		result = result.groupdict()
		item = Item(result["item"].strip())
		item_id = result["item_id"]
		value = int(result["value"])
		return (item, item_id, value)

	def parse_file(self, filename):
		with open(filename) as f:
			for (lineno, line) in enumerate(f, 1):
				line = line.rstrip("\r\n")
				if line.startswith("#") or line.strip() == "":
					continue
				(item, item_id, value) = self._parse_line(line)
				self.add(item, item_id, value)
		return self
