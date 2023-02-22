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

import enum
import dataclasses

class ProductionRateDisplay(enum.IntEnum):
	CombinedProductionRate = 0
	SplitRecipeProductionRate = 1
	RecipeOnlyProductionRate = 2

class RateSuffix(enum.Enum):
	UnitSuffix = ""
	UnitsPerSecond = "/sec"
	UnitsPerMinute = "/min"

class EntityCardinalityFormat(enum.IntEnum):
	RoundedCeiling = 0
	FloatingPoint = 1
	Fractioanl = 2

@dataclasses.dataclass
class DisplayPreferences():
	rate_suffix: RateSuffix = RateSuffix("")
	production_rate_display: ProductionRateDisplay = ProductionRateDisplay.CombinedProductionRate
	entity_cardinality_format: EntityCardinalityFormat = EntityCardinalityFormat.RoundedCeiling
