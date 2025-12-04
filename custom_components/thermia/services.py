"""Thermia services setup class."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.service import async_extract_entity_ids
from homeassistant.helpers import device_registry as dr

from .coordinator import ThermiaDataUpdateCoordinator
from .const import DEBUG_ACTION_NAME, DEFAULT_DEBUG_FILENAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


class ThermiaServicesSetup:
    """Set up Thermia services."""

    def __init__(self, hass: HomeAssistant, coordinator: ThermiaDataUpdateCoordinator):
        self.hass = hass
        self.coordinator = coordinator

        self.setup_services()

    def setup_services(self):
        """Set up Thermia services."""
        self.hass.services.async_register(
            DOMAIN, DEBUG_ACTION_NAME, self.async_handle_heat_pump_debug
        )

    async def async_handle_heat_pump_debug(self, call: ServiceCall):
        """Handle debug service call."""
        entity_ids = await async_extract_entity_ids(self.hass, call)

        # Only allow 1 water heater entity
        entity_ids = [
            e for e in entity_ids if e.startswith("water_heater.")
        ]

        if len(entity_ids) != 1:
            raise ServiceValidationError(
                "Exactly one water heater entity should be provided"
            )

        entity_id = entity_ids[0]

        #
        # 🔧 Get device identifiers using the device registry (HA-supported)
        #
        device_registry = dr.async_get(self.hass)
        device = device_registry.async_get_device(
            identifiers=None,
            connections=None,
            entity_id=entity_id,
        )

        if device is None:
            raise ServiceValidationError(
                f"Cannot find device for entity {entity_id}"
            )

        if not device.identifiers or len(device.identifiers) != 1:
            raise ServiceValidationError(
                f"Invalid or missing device identifiers for entity {entity_id}"
            )

        # identifiers is a set → {("domain", "device_id")}
        domain, heat_pump_id = next(iter(device.identifiers))

        #
        # 🔍 Locate the heat pump in coordinator data
        #
        heat_pump = next(
            (
                hp
                for hp in self.coordinator.data.heat_pumps
                if hp.id == heat_pump_id
            ),
            None,
        )

        if heat_pump is None:
            raise ServiceValidationError("Cannot find heat pump by unique_id")

        #
        # 📄 Collect debug information
        #
        debug_data = await self.hass.async_add_executor_job(
            lambda: heat_pump.debug()
        )

        def create_debug_file():
            with open(DEFAULT_DEBUG_FILENAME, "w", encoding="utf-8") as report_file:
                report_file.write(debug_data)

            _LOGGER.info(
                f"Thermia debug file created: {DEFAULT_DEBUG_FILENAME}"
            )

        await self.hass.async_add_executor_job(create_debug_file)

