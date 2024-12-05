"""Thermia Generic Sensor integration."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinator import ThermiaDataUpdateCoordinator


class ThermiaGenericSensor(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], SensorEntity
):
    """Representation of an Thermia generic sensor."""

    def __init__(
        self,
        coordinator,
        idx,
        is_online_prop: str,
        sensor_name: str,
        mdi_icon: str,
        entity_category: str,
        device_class: str | None,
        state_class: str,
        value_prop: str,
        unit_of_measurement: str | None,
    ):
        super().__init__(coordinator)
        self.idx: int = idx

        self._is_online_prop: str = is_online_prop
        self._sensor_name: str = sensor_name
        self._mdi_icon: str = mdi_icon
        self._entity_category: str = entity_category
        self._device_class: str | None = device_class
        self._state_class: str = state_class
        self._value_prop: str = value_prop
        self._unit_of_measurement: str | None = unit_of_measurement

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
            "model_id": self.coordinator.data.heat_pumps[self.idx].model_id,
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
        """Return value of the sensor."""
        return getattr(self.coordinator.data.heat_pumps[self.idx], self._value_prop)

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement
