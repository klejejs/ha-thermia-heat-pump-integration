"""Thermia Generic Sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN


class ThermiaGenericSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Thermia generic sensor."""

    def __init__(
        self,
        coordinator,
        idx,
        is_online_prop,
        sensor_name,
        mdi_icon,
        entity_category,
        device_class,
        state_class,
        value_prop,
        unit_of_measurement,
    ):
        super().__init__(coordinator)
        self.idx = idx

        self._is_online_prop = is_online_prop
        self._sensor_name = sensor_name
        self._mdi_icon = mdi_icon
        self._entity_category = entity_category
        self._device_class = device_class
        self._state_class = state_class
        self._value_prop = value_prop
        self._unit_of_measurement = unit_of_measurement

    @property
    def available(self):
        """Return True if entity is available."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._is_online_prop)

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name} {self._sensor_name}"

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return f"{self.coordinator.data.heat_pumps[self.idx].name}_{self._sensor_name.lower().replace(' ', '_')}"

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
    def entity_category(self):
        """Return the category of the sensor."""
        return self._entity_category

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        return self._state_class

    @property
    def native_value(self):
        """Return active alarms count of the sensor."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._value_prop)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement
