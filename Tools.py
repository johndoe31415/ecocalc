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

import fractions

class NumberTools():
	@classmethod
	def str2num(cls, text):
		if isinstance(text, str):
			try:
				return int(text)
			except ValueError:
				pass
		return fractions.Fraction(text)

	@classmethod
	def num2str(cls, number):
		real_value = float(number)
		formats = [
			lambda value: (round(value), "%d"),
			lambda value: (round(value, 1), "%.1f"),
			lambda value: (round(value, 2), "%.2f"),
		]
		for format_fnc in formats:
			(formatted_value, format_str) = format_fnc(real_value)
			if abs(formatted_value - real_value) < 0.01:
				return format_str % formatted_value
		return "%.3f" % (real_value)
