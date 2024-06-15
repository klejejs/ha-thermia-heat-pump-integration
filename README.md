# Thermia Heat Pump Integration

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/klejejs/ha-thermia-heat-pump-integration?style=for-the-badge)](https://github.com/klejejs/ha-thermia-heat-pump-integration/releases)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/klejejs/ha-thermia-heat-pump-integration?style=for-the-badge)](https://github.com/klejejs/ha-thermia-heat-pump-integration/commits)
[![License](https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge)](LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Thermia Heat Pump Integration for Home Assistant. Depends on [Python Thermia Online API](https://github.com/klejejs/python-thermia-online-api).

_Component to integrate with [Thermia Heat Pump](https://github.com/klejejs/ha-thermia-heat-pump-integration)._

**This component will set up the following platforms.**

Platform | Description
-- | --
`water_heater` | Thermia Heat Pump integration
`sensor` | Thermia Outside Temperature sensor (if available)
`switch` | Thermia Heat Pump Hot Water Switch (if available)

## Confirmed Thermia profiles that API supports:
* Thermia Diplomat / Diplomat Duo
* Thermia iTec


## Confirmed Thermia models that API supports:
* Danfoss DHP-AQ 9
* Calibra Duo
* Atec

## Setup

To set up Thermia Heat Pump Integration, go to Settings -> Integrations -> Add Integration and search for Thermia Heat Pump.

Depending on the url you use to see your heat pump online, you need to choose the following API type:
* `classic` - for url: https://online.thermia.se
* `genesis` - for url: https://online-genesis.thermia.se

## Installation

Open HACS, go to the Integrations view and search for Thermia Heat Pump Integration.

## Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `thermia_water_heater`.
4. Download _all_ the files from the `custom_components/thermia_water_heater/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/thermia_water_heater/__init__.py
custom_components/thermia_water_heater/manifest.json
custom_components/thermia_water_heater/water_heater.py
```

---

## Contributions are welcome!
