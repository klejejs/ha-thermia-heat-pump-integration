"""Thermia water heater class."""

from __future__ import annotations

import logging

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    SUPPORT_OPERATION_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import (
    ATTR_TEMPERATURE,
    TEMP_CELSIUS,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia water heater."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_water_heaters = [
        ThermiaWaterHeater(coordinator, idx)
        for idx, _ in enumerate(coordinator.data.heat_pumps)
    ]

    async_add_entities(hass_water_heaters)


class ThermiaWaterHeater(CoordinatorEntity, WaterHeaterEntity):
    """Representation of an Thermia water heater."""

    def __init__(self, coordinator, idx):
        super().__init__(coordinator)
        self.idx = idx

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data.heat_pumps[self.idx].is_online

    @property
    def name(self):
        """Return the name of the water heater."""
        return self.coordinator.data.heat_pumps[self.idx].name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self.coordinator.data.heat_pumps[self.idx].id

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:water-pump"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.data.heat_pumps[self.idx].id)},
            "name": self.coordinator.data.heat_pumps[self.idx].name,
            "manufacturer": "Thermia",
            "model": self.coordinator.data.heat_pumps[self.idx].model,
        }

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        default_min_temp = 0

        if not self.available:
            return default_min_temp

        min_temp = self.coordinator.data.heat_pumps[self.idx].heat_min_temperature_value

        if min_temp is not None:
            return min_temp
        return default_min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        default_max_temp = 50

        if not self.available:
            return default_max_temp

        max_temp = self.coordinator.data.heat_pumps[self.idx].heat_max_temperature_value

        if max_temp is not None:
            return max_temp
        return default_max_temp

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self.coordinator.data.heat_pumps[self.idx].indoor_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self.coordinator.data.heat_pumps[self.idx].heat_temperature

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def current_operation(self):
        """Return current operation ie. eco, off, etc."""
        return self.coordinator.data.heat_pumps[self.idx].operation_mode

    @property
    def operation_list(self):
        """List of available operation modes."""
        return self.coordinator.data.heat_pumps[self.idx].available_operation_modes

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is not None:
            await self.hass.async_add_executor_job(
                lambda: self.coordinator.data.heat_pumps[self.idx].set_temperature(
                    target_temp
                )
            )
        else:
            _LOGGER.error("A target temperature must be provided")

    async def async_set_operation_mode(self, operation_mode):
        """Set operation mode."""
        if operation_mode is not None:
            await self.hass.async_add_executor_job(
                lambda: self.coordinator.data.heat_pumps[self.idx].set_operation_mode(
                    operation_mode
                )
            )
        else:
            _LOGGER.error("An operation mode must be provided")
