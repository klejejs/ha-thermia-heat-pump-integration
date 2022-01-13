"""Thermia switch integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .switches.hot_water_switch import ThermiaHotWaterSwitch

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia switches."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_hot_water_switches = [
        ThermiaHotWaterSwitch(coordinator, idx)
        for idx, heat_pump in enumerate(coordinator.data.heat_pumps)
        if heat_pump.is_hot_water_switch_available
        and heat_pump.hot_water_switch_state is not None
    ]

    async_add_entities(hass_thermia_hot_water_switches)
