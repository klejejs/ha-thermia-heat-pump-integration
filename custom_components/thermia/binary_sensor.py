"""Thermia binary sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from .binary_sensors.operational_status_binary_sensor import (
    ThermiaOperationalStatusBinarySensor,
)

from .const import (
    DOMAIN,
    MDI_INFORMATION_OUTLINE_ICON,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia binary sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_binary_sensors = []

    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        if heat_pump.operational_status_compressor_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Compressor Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_compressor_status",
                )
            )

        if heat_pump.operational_status_brine_pump_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Brine Pump Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_brine_pump_status",
                )
            )

        if heat_pump.operational_status_radiator_pump_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Radiator Pump Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_radiator_pump_status",
                )
            )

        if heat_pump.operational_status_cooling_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Cooling Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_cooling_status",
                )
            )

        if heat_pump.operational_status_hot_water_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Hot Water Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_hot_water_status",
                )
            )

        if heat_pump.operational_status_heating_status is not None:
            hass_thermia_binary_sensors.append(
                ThermiaOperationalStatusBinarySensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Heating Status",
                    MDI_INFORMATION_OUTLINE_ICON,
                    BinarySensorDeviceClass.POWER,
                    "operational_status_heating_status",
                )
            )

    async_add_entities(hass_thermia_binary_sensors)
