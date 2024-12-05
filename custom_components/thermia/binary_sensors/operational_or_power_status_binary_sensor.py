"""Thermia Operational Status Binary Sensor integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DOMAIN
from ..coordinator import ThermiaDataUpdateCoordinator


class ThermiaOperationalOrPowerStatusBinarySensor(
    CoordinatorEntity[ThermiaDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of an Thermia Operational or Power Status binary sensor."""

    def __init__(
        self,
        coordinator,
        idx: int,
        is_online_prop: str,
        binary_sensor_name: str,
        mdi_icon: str,
        device_class: BinarySensorDeviceClass,
        status_value: str,
        running_status_list: str,
    ):
        super().__init__(coordinator)
        self.idx: int = idx

        self._is_online_prop: str = is_online_prop
        self._binary_sensor_name: str = binary_sensor_name
        self._mdi_icon: str = mdi_icon
        self._device_class: BinarySensorDeviceClass = device_class
        self._status_value: str = status_value
        self._running_status_list: str = running_status_list

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
            "model_id": self.coordinator.data.heat_pumps[self.idx].model_id,
        }

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def is_on(self):
        """Return the state of the sensor."""
        heat_pump = self.coordinator.data.heat_pumps[self.idx]

        return self._status_value in getattr(heat_pump, self._running_status_list)
