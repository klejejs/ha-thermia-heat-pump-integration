"""Thermia active alarms sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN


class ThermiaActiveAlarmsSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Thermia active alarms sensor."""

    def __init__(self, coordinator, idx):
        super().__init__(coordinator)
        self.idx = idx

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.data.connected

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} Active Alarms"

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_active_alarms"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:bell-alert"

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
    def state_class(self):
        """Return the state class."""
        return "total"

    @property
    def native_value(self):
        """Return active alarms count of the sensor."""
        return self.coordinator.data.heat_pumps[self.idx].active_alarm_count
