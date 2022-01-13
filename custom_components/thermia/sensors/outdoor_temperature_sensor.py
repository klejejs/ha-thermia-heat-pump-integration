"""Thermia outdoor temperature sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN


class ThermiaOutdoorTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Thermia outdoor temperature sensor."""

    def __init__(self, coordinator, idx):
        super().__init__(coordinator)
        self.idx = idx

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data.heat_pumps[self.idx].is_online

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} Outdoor Temperature"

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_outdoor_temperature"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:thermometer"

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
        """Return the device class."""
        return "temperature"

    @property
    def state_class(self):
        """Return the state class."""
        return "measurement"

    @property
    def native_value(self):
        """Return the temperature of the sensor."""
        return self.coordinator.data.heat_pumps[self.idx].outdoor_temperature

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return TEMP_CELSIUS

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()
