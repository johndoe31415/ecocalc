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

import json
import logging
from .Resource import Resource
from .ProductionEntity import ProductionEntity
from .ProductionEntityGroup import ProductionEntityGroup
from .RateScalar import RateScalar
from .Recipe import Recipe
from .Exceptions import DuplicateResourceNameException, UnknownResourceException
from .Tools import IterTools

_log = logging.getLogger(__spec__.name)

class EconomyDefinition():
	def __init__(self, resources: dict, production_entities: dict, production_entity_groups: dict, rate_scalars: dict, recipes: list):
		self._resources = resources
		self._production_entities = production_entities
		self._production_entity_groups = production_entity_groups
		self._rate_scalars = rate_scalars
		self._recipes = recipes
		self._register_economy()
		self._plausibility_check()

	def _register_economy(self):
		for recipe in self._recipes:
			recipe.economy = self

	def _plausibility_check(self):
		duplicate_resource_names = IterTools.duplicates(resource.name for resource in self._resources.values())
		if len(duplicate_resource_names) > 0:
			raise DuplicateResourceNameException(f"Duplicate resource name found: {', '.join(sorted(duplicate_resource_names))}")

		resource_ids = set(self._resources)
		for recipe in self._recipes:
			unknown_ingredients = recipe.ingredients - resource_ids
			if len(unknown_ingredients) > 0:
				raise UnknownResourceException(f"Recipe \"{recipe}\" has {len(unknown_ingredients)} unknown ingredient(s): {', '.join(sorted(unknown_ingredients))}")

	@property
	def recipes(self):
		return iter(self._recipes)

	def get_resource_name(self, resource_identifier):
		if not self.has_resource(resource_identifier):
			return resource_identifier
		else:
			return self.get_resource(resource_identifier).name

	def has_resource(self, resource_identifier):
		return resource_identifier in self._resources

	def get_resource(self, resource_identifier):
		return self._resources[resource_identifier]

	def has_production_entity(self, production_entity_identifier):
		return production_entity_identifier in self._production_entitys

	def get_production_entity(self, production_entity_identifier):
		return self._production_entities[production_entity_identifier]

	def has_rate_scalar(self, rate_scalar_identifier):
		return rate_scalar_identifier in self._rate_scalars

	def get_rate_scalar(self, rate_scalar_identifier):
		return self._rate_scalars[rate_scalar_identifier]

	def has_production_entity_group(self, production_entity_group_identifier):
		return production_entity_group_identifier in self._production_entity_groups

	def get_production_entity_group(self, production_entity_group_identifier):
		return self._production_entity_groups[production_entity_group_identifier]

	@classmethod
	def load_from_json(cls, filename: str):
		with open(filename) as f:
			data = json.load(f)

		resources = { resource_id: Resource.from_dict(resource_id, resource_definition) for (resource_id, resource_definition) in data["resources"].items() }
		production_entities = { production_entity_id: ProductionEntity.from_dict(production_entity_id, production_entity_definition) for (production_entity_id, production_entity_definition) in data["production_entities"].items() }
		production_entity_groups = { production_entity_group_id: ProductionEntityGroup.from_list(production_entity_group_id, production_entity_group_definition) for (production_entity_group_id, production_entity_group_definition) in data["production_entity_groups"].items() }
		rate_scalars = { rate_scalar_id: RateScalar.from_dict(rate_scalar_definition) for (rate_scalar_id, rate_scalar_definition) in data["rate_scalars"].items() }
		recipes = [ Recipe.from_dict(recipe_definition) for recipe_definition in data["recipes"] ]
		return cls(resources = resources, production_entities = production_entities, production_entity_groups = production_entity_groups, rate_scalars = rate_scalars, recipes = recipes)
