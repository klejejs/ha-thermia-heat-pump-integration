"""Thermia heat pump integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ThermiaOnlineAPI import Thermia
from ThermiaOnlineAPI.api.ThermiaAPI import ThermiaAPI

from .const import API_TYPE, API_TYPE_CLASSIC, CONF_PASSWORD, CONF_USERNAME, DOMAIN

PLATFORMS: list[str] = ["sensor", "switch", "water_heater"]


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
    api_type = config_entry.data.get(API_TYPE, API_TYPE_CLASSIC)

    thermia = await hass.async_add_executor_job(
        lambda: Thermia(username, password, api_type)
    )

    coordinator = ThermiaDataUpdateCoordinator(hass, thermia)

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(config_entry, PLATFORMS)

    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ThermiaDataUpdateCoordinator(DataUpdateCoordinator):
    """Thermia Data Update Coordinator."""

    def __init__(self, hass: HomeAssistant, thermia: ThermiaAPI):
        """Initialize the data update object."""

        self.thermia = thermia

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self):
        """Update the data."""
        try:
            await self.hass.async_add_executor_job(lambda: self.thermia.update_data())
        except Exception as exception:
            raise UpdateFailed(exception)

        return self.thermia


async def async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
