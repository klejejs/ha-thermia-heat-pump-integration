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

        self._attr_available = getattr(
            self.coordinator.data.heat_pumps[self.idx], is_online_prop
        )
        self._attr_name = (
            f"{self.coordinator.data.heat_pumps[self.idx].name} {sensor_name}"
        )
        self._attr_unique_id = f"{self.coordinator.data.heat_pumps[self.idx].name}_{sensor_name.lower().replace(' ', '_')}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self.coordinator.data.heat_pumps[self.idx].id)},
            "name": self.coordinator.data.heat_pumps[self.idx].name,
            "manufacturer": "Thermia",
            "model": self.coordinator.data.heat_pumps[self.idx].model,
        }
        self._attr_icon = mdi_icon
        self._attr_entity_category = entity_category
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_native_value = getattr(
            self.coordinator.data.heat_pumps[self.idx], value_prop
        )
        self._attr_unit_of_measurement = unit_of_measurement

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()
