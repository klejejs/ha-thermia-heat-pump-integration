"""Thermia sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensors.active_alarms_sensor import ThermiaActiveAlarmsSensor
from .sensors.outdoor_temperature_sensor import ThermiaOutdoorTemperatureSensor

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_outdoor_temperature_sensors = [
        ThermiaOutdoorTemperatureSensor(coordinator, idx)
        for idx, heat_pump in enumerate(coordinator.data.heat_pumps)
        if heat_pump.is_outdoor_temp_sensor_functioning
        and heat_pump.outdoor_temperature
    ]

    hass_thermia_active_alarms_sensors = [
        ThermiaActiveAlarmsSensor(coordinator, idx)
        for idx, _ in enumerate(coordinator.data.heat_pumps)
    ]

    async_add_entities(
        [*hass_thermia_outdoor_temperature_sensors, *hass_thermia_active_alarms_sensors]
    )
