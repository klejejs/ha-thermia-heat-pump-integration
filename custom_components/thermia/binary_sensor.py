"""Thermia binary sensor integration."""

from __future__ import annotations
from typing import List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from .binary_sensors.operational_or_power_status_binary_sensor import (
    ThermiaOperationalOrPowerStatusBinarySensor,
)
from ThermiaOnlineAPI import ThermiaHeatPump

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

    heat_pumps: List[ThermiaHeatPump] = coordinator.data.heat_pumps

    for idx, heat_pump in enumerate(heat_pumps):
        if heat_pump.available_operational_statuses is not None and heat_pump.running_operational_statuses is not None:
            for operational_status in heat_pump.available_operational_statuses:
                name = operational_status.replace("_", " ").title()
                hass_thermia_binary_sensors.append(
                    ThermiaOperationalOrPowerStatusBinarySensor(
                        coordinator,
                        idx,
                        "is_online",
                        f"{name} Operational Status",
                        MDI_INFORMATION_OUTLINE_ICON,
                        BinarySensorDeviceClass.RUNNING,
                        operational_status,
                        "running_operational_statuses"
                    )
                )

        if heat_pump.available_power_statuses is not None and heat_pump.running_power_statuses is not None:
            for power_status in heat_pump.available_power_statuses:
                name = power_status.replace("_", " ").title()
                hass_thermia_binary_sensors.append(
                    ThermiaOperationalOrPowerStatusBinarySensor(
                        coordinator,
                        idx,
                        "is_online",
                        f"{name} Power Status",
                        MDI_INFORMATION_OUTLINE_ICON,
                        BinarySensorDeviceClass.RUNNING,
                        power_status,
                        "running_power_statuses"
                    )
                )

    async_add_entities(hass_thermia_binary_sensors)
