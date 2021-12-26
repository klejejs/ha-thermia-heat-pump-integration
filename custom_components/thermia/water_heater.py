import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from homeassistant.components.water_heater import WaterHeaterEntity

from homeassistant.components.water_heater import (
  PLATFORM_SCHEMA,
  SUPPORT_OPERATION_MODE,
  SUPPORT_TARGET_TEMPERATURE,
)

from homeassistant.const import (
  ATTR_TEMPERATURE,
  CONF_PASSWORD,
  CONF_USERNAME,
  TEMP_CELSIUS,
)

from ThermiaOnlineAPI import Thermia

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'thermia'

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Required(CONF_USERNAME): cv.string,
  vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
  """Set up the Thermia heat pumps as water heaters."""

  username = config.get(CONF_USERNAME)
  password = config.get(CONF_PASSWORD)

  thermia = Thermia(username, password)
  heat_pumps = thermia.heat_pumps
  hass_water_heaters = [
    ThermiaWaterHeater(heat_pump) for heat_pump in heat_pumps
  ]
  add_entities(hass_water_heaters)


class ThermiaWaterHeater(WaterHeaterEntity):
  """Representation of an Thermia water heater."""

  def __init__(self, water_heater):
    self.water_heater = water_heater

  @property
  def name(self):
    """Return the name of the water heater."""
    return self.water_heater.name

  @property
  def unique_id(self):
    """Return a unique ID."""
    return self.water_heater.id

  @property
  def min_temp(self):
    """Return the minimum temperature."""
    return self.water_heater.heat_min_temperature_value

  @property
  def max_temp(self):
    """Return the maximum temperature."""
    return self.water_heater.heat_max_temperature_value

  @property
  def current_temperature(self):
    """Return the current temperature."""
    return self.water_heater.indoor_temperature

  @property
  def target_temperature(self):
    """Return the temperature we try to reach."""
    return self.water_heater.heat_temperature

  @property
  def temperature_unit(self):
    """Return the unit of measurement."""
    return TEMP_CELSIUS

  @property
  def current_operation(self):
    """Return current operation ie. eco, off, etc."""
    return self.water_heater.operation_mode

  @property
  def operation_list(self):
    """List of available operation modes."""
    return self.water_heater.available_operation_modes

  @property
  def supported_features(self):
    """Return the list of supported features."""
    return SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE

  def set_temperature(self, **kwargs):
    """Set new target temperature."""
    target_temp = kwargs.get(ATTR_TEMPERATURE)
    if target_temp is not None:
      self.water_heater.set_temperature(target_temp)
    else:
      _LOGGER.error("A target temperature must be provided")

  def set_operation_mode(self, operation_mode):
    """Set operation mode."""
    if operation_mode is not None:
      self.water_heater.set_operation_mode(operation_mode)
    else:
      _LOGGER.error("An operation mode must be provided")

  def update(self):
    """Update the state of the water heater."""
    self.water_heater.refetch_data()
