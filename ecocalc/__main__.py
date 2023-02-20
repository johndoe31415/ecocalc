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

import sys
import logging
from .FriendlyArgumentParser import FriendlyArgumentParser
from .EconomyDefinition import EconomyDefinition

def setup_logging(verbosity = 0):
	if verbosity == 0:
		loglevel = logging.WARN
	elif verbosity == 1:
		loglevel = logging.INFO
	elif verbosity == 2:
		loglevel = logging.DEBUG
	elif verbosity == 3:
		loglevel = logging.TRACE
	else:
		loglevel = logging.SINGLESTEP
	logging.basicConfig(format = "{name:>30s} [{levelname:.1s}]: {message}", style = "{", level = loglevel)

def main():
	parser = FriendlyArgumentParser(description = "Economy calculation for factory-building games")
	parser.add_argument("-e", "--economy-definition", metavar = "filename", required = True, help = "Specifies the economy definition file. Mandatory argument.")
	parser.add_argument("--computation-mode", choices = [ "rate", "count" ], default = "rate", help = "Specifies whether to compute production rate (e.g., items per time unit) or production count (i.e., numer of items). Can be one of %(choices)s, defaults to %(default)s.")
	parser.add_argument("--rate-unit", choices = [ "upm", "ups" ], default = "upm", help = "Production rate unit. Can be either units/minute (upm) or units/secons (ups), i.e, one of %(choices)s, defaults to %(default)s.")
	parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
	parser.add_argument("prod_specifier", nargs = "+", help = "Production specifier(s).")
	args = parser.parse_args(sys.argv[1:])

	setup_logging(args.verbose)
	eco = EconomyDefinition.load_from_json(args.economy_definition)

if __name__ == "__main__":
	sys.exit(main())
