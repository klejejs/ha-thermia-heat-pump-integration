"""Thermia sensor integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import TEMP_CELSIUS, TIME_HOURS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .sensors.active_alarms_sensor import ThermiaActiveAlarmsSensor
from .sensors.generic_sensor import ThermiaGenericSensor

from .const import (
    DOMAIN,
    MDI_TEMPERATURE_ICON,
    MDI_TIMER_COG_OUTLINE_ICON,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Thermia sensors."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    hass_thermia_sensors = []

    for idx, heat_pump in enumerate(coordinator.data.heat_pumps):
        if (
            heat_pump.is_outdoor_temp_sensor_functioning
            and heat_pump.outdoor_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Outdoor Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "outdoor_temperature",
                    TEMP_CELSIUS,
                )
            )

        if (
            heat_pump.has_indoor_temp_sensor
            and heat_pump.indoor_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Indoor Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "indoor_temperature",
                    TEMP_CELSIUS,
                )
            )

        if (
            heat_pump.is_hot_water_active
            and heat_pump.hot_water_temperature is not None
        ):
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Hot Water Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "hot_water_temperature",
                    TEMP_CELSIUS,
                )
            )

        ###########################################################################
        # Other temperature sensors
        ###########################################################################

        if heat_pump.supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "supply_line_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.desired_supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Desired Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "desired_supply_line_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.return_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Return Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "return_line_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.brine_out_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Brine Out Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "brine_out_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.brine_in_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Brine In Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "brine_in_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.cooling_tank_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Cooling Tank Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "cooling_tank_temperature",
                    TEMP_CELSIUS,
                )
            )

        if heat_pump.cooling_supply_line_temperature is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Cooling Supply Line Temperature",
                    MDI_TEMPERATURE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    "temperature",
                    "measurement",
                    "cooling_supply_line_temperature",
                    TEMP_CELSIUS,
                )
            )

        ###########################################################################
        # Operational status data
        ###########################################################################

        if heat_pump.operational_status is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Operational Status",
                    "mdi:thermostat",
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "measurement",
                    "operational_status",
                    None,
                )
            )

        ###########################################################################
        # Operational time data
        ###########################################################################

        if heat_pump.compressor_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Compressor Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "compressor_operational_time",
                    TIME_HOURS,
                )
            )

        if heat_pump.hot_water_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Hot Water Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "hot_water_operational_time",
                    TIME_HOURS,
                )
            )

        if heat_pump.auxiliary_heater_1_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 1 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_1_operational_time",
                    TIME_HOURS,
                )
            )

        if heat_pump.auxiliary_heater_2_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 2 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_2_operational_time",
                    TIME_HOURS,
                )
            )

        if heat_pump.auxiliary_heater_3_operational_time is not None:
            hass_thermia_sensors.append(
                ThermiaGenericSensor(
                    coordinator,
                    idx,
                    "is_online",
                    "Auxiliary Heater 3 Operational Time",
                    MDI_TIMER_COG_OUTLINE_ICON,
                    EntityCategory.DIAGNOSTIC,
                    None,
                    "total_increasing",
                    "auxiliary_heater_3_operational_time",
                    TIME_HOURS,
                )
            )

    hass_thermia_active_alarms_sensors = [
        ThermiaActiveAlarmsSensor(coordinator, idx)
        for idx, _ in enumerate(coordinator.data.heat_pumps)
    ]

    async_add_entities([*hass_thermia_active_alarms_sensors, *hass_thermia_sensors])
