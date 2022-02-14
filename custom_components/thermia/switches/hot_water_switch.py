"""Thermia hot water switch integration."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN


class ThermiaHotWaterSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of an Thermia hot water switch."""

    def __init__(self, coordinator, idx):
        super().__init__(coordinator)
        self.idx = idx

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data.heat_pumps[self.idx].is_online

    @property
    def name(self):
        """Return the name of the switch."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} Hot Water"

    @property
    def unique_id(self):
        """Return the unique ID of the switch."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_hot_water"

    @property
    def icon(self):
        """Return the icon of the switch."""
        return "mdi:water-boiler"

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
    def device_class(self):
        """Return the device class of the switch."""
        return "switch"

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.coordinator.data.heat_pumps[self.idx].hot_water_switch_state == 1

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.hass.async_add_executor_job(
            lambda: self.coordinator.data.heat_pumps[
                self.idx
            ].set_hot_water_switch_state(1)
        )

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.hass.async_add_executor_job(
            lambda: self.coordinator.data.heat_pumps[
                self.idx
            ].set_hot_water_switch_state(0)
        )

    async def async_toggle(self, **kwargs):
        """Toggle the switch."""
        if self.is_on:
            await self.async_turn_off()
        else:
            await self.async_turn_on()
