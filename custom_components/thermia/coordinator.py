from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from ThermiaOnlineAPI import Thermia

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ThermiaDataUpdateCoordinator(DataUpdateCoordinator[Thermia]):
    """Thermia Data Update Coordinator."""

    def __init__(self, hass: HomeAssistant, thermia: Thermia):
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
