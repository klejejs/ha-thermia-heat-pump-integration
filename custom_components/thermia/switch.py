"""Thermia switch integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .switches.hot_water_switch import ThermiaHotWaterSwitch
from .switches.hot_water_boost_switch import ThermiaHotWaterBoostSwitch

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia switches."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_switches = []

    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        if heat_pump.hot_water_switch_state is not None:
            hass_thermia_switches.append(ThermiaHotWaterSwitch(coordinator, idx))

        if heat_pump.hot_water_boost_switch_state is not None:
            hass_thermia_switches.append(ThermiaHotWaterBoostSwitch(coordinator, idx))

    async_add_entities(hass_thermia_switches)
