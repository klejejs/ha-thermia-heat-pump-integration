"""Thermia services setup class."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.service import async_extract_entity_ids
from homeassistant.helpers.template import device_attr

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

        entity_ids = list(
            filter(lambda entity_id: entity_id.startswith("water_heater."), entity_ids)
        )

        if len(entity_ids) == 0 or len(entity_ids) > 1:
            raise ServiceValidationError(
                "Exactly one water heater entity should be provided"
            )

        entity_id = entity_ids[0]

        device_identifiers = device_attr(self.hass, entity_id, "identifiers")

        if device_identifiers is None:
            raise ServiceValidationError(
                f"Cannot find device identifiers for entity {entity_id}"
            )

        device_identifiers = list(device_identifiers)

        if len(device_identifiers) != 1 and len(device_identifiers[0]) != 2:
            raise ServiceValidationError(
                f"Invalid device identifiers for entity {entity_id}"
            )

        heat_pump_id = device_identifiers[0][1]

        heat_pump = next(
            (
                heat_pump
                for heat_pump in self.coordinator.data.heat_pumps
                if heat_pump.id == heat_pump_id
            ),
            None,
        )

        if heat_pump is None:
            raise ServiceValidationError("Cannot find heat pump by unique_id")

        debug_data = await self.hass.async_add_executor_job(lambda: heat_pump.debug())

        def create_debug_file():
            with open(DEFAULT_DEBUG_FILENAME, "w", encoding="utf-8") as report_file:
                report_file.write(debug_data)

            _LOGGER.info(
                f"Thermia debug file was created and data was written to {
                    DEFAULT_DEBUG_FILENAME}"
            )

        await self.hass.async_add_executor_job(create_debug_file)
