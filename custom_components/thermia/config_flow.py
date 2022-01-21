"""Config Flow for Thermia."""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from ThermiaOnlineAPI import AuthenticationException, Thermia

from .const import (
    API_TYPE,
    API_TYPE_CLASSIC,
    API_TYPES,
    CONF_PASSWORD,
    CONF_USERNAME,
    DOMAIN,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Required(API_TYPE, default=API_TYPE_CLASSIC): vol.In(API_TYPES),
    }
)

_LOGGER = logging.getLogger(__name__)


class ThermiaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Thermia Config Flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def _check_credentials(self, user_input):
        """Check if Thermia credentials are valid."""
        try:
            thermia = await self.hass.async_add_executor_job(
                lambda: Thermia(
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    user_input[API_TYPE],
                )
            )
            await self.hass.async_add_executor_job(thermia.fetch_heat_pumps)
        except Exception as error:
            _LOGGER.error(error)
            self._errors["base"] = "invalid_credentials"
            raise AuthenticationException(error)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            try:
                await self._check_credentials(user_input)
                return self.async_create_entry(
                    title=f"Thermia ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )
            except Exception:
                pass

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=self._errors,
        )
