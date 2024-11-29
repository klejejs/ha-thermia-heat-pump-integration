"""Thermia heat pump integration."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType
from ThermiaOnlineAPI import Thermia

from .const import CONF_PASSWORD, CONF_USERNAME, DEBUG_ACTION_NAME, DOMAIN
from .coordinator import ThermiaDataUpdateCoordinator
from .services import ThermiaServicesSetup

PLATFORMS: list[str] = ["binary_sensor", "sensor", "switch", "water_heater"]


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType):
    """Set up the Thermia component."""
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up the Thermia heat pumps."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    username = config_entry.data[CONF_USERNAME]
    password = config_entry.data[CONF_PASSWORD]

    thermia = await hass.async_add_executor_job(lambda: Thermia(username, password))

    coordinator = ThermiaDataUpdateCoordinator(hass, thermia)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)

    config_entry.async_on_unload(
        config_entry.add_update_listener(async_reload_entry))

    ThermiaServicesSetup(hass, coordinator)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(
                    entry, component)
                for component in PLATFORMS
            ]
        )
    )

    if hass.services.has_service(DOMAIN, DEBUG_ACTION_NAME):
        hass.services.async_remove(DOMAIN, DEBUG_ACTION_NAME)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
