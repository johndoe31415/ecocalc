#!/usr/bin/python3
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

import sys

def to_item(x):
	if " " in x:
		x = x.split()
		return (int(x[0]), x[1])
	else:
		return (1, x)

infile = sys.argv[1]
with open(infile) as f, open("output_economy.txt", "w") as ecofile, open("output_recipes.txt", "w") as recipefile:
	values = { }
	for line in f:
		line = line.strip()
		if line == "":
			print(file = recipefile)
			continue

		if "=" not in line:
			(item, value) = line.split()
			value = int(value)
			if item not in values:
				values[item] = value
			else:
				if not values[item] == value:
					raise Exception("%s has value %d and %d." % (item, values[item], value))
		else:
			(src, dst) = line.split("=")
			(dst, value) = dst.split("(")
			value = int(value.rstrip(")"))
			src = [ to_item(x) for x in src.split("+") ]
			if dst not in values:
				values[dst] = value
			else:
				if not values[dst] == value:
					raise Exception("%s has value %d and %d." % (dst, values[dst], value))
			values[dst]
			print("%s -> 1 %s" % (" + ".join("%d %s" % (cnt, value) for (cnt, value) in src), dst), file = recipefile)
	for (item, value) in sorted(values.items()):
		print("%s = %d" % (item, value), file = ecofile)
