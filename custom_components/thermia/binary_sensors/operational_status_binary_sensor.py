"""Thermia Operational Status Binary Sensor integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN


class ThermiaOperationalStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of an Thermia Operational Status binary sensor."""

    def __init__(
        self,
        coordinator,
        idx,
        is_online_prop,
        binary_sensor_name,
        mdi_icon,
        device_class,
        value_prop,
    ):
        super().__init__(coordinator)
        self.idx = idx

        self._is_online_prop = is_online_prop
        self._binary_sensor_name = binary_sensor_name
        self._mdi_icon = mdi_icon
        self._device_class = device_class
        self._value_prop = value_prop

    @property
    def available(self):
        """Return True if entity is available."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._is_online_prop)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} {self._binary_sensor_name}"

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_{self._binary_sensor_name.lower().replace(' ', '_')}"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._mdi_icon

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
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def is_on(self):
        """Return the state of the sensor."""
        heat_pump = self.coordinator.data.heat_pumps[self.idx]

        return getattr(heat_pump, self._value_prop)
