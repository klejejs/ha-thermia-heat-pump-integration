# Thermia Heat Pump Integration

[![GitHub Release](https://img.shields.io/github/release/custom-components/blueprint.svg?style=for-the-badge)](https://github.com/klejejs/ha-thermia-heat-pump-integration/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/custom-components/blueprint.svg?style=for-the-badge)](https://github.com/klejejs/ha-thermia-heat-pump-integration/commits/main)
[![License](https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge)](LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Thermia Heat Pump Integration for Home Assistant

_Component to integrate with [Thermia Heat Pump](https://github.com/klejejs/ha-thermia-heat-pump-integration)._

**This component will set up the following platforms.**

Platform | Description
-- | --
`water_heater` | Thermia Heat Pump integration

## Setup

To set up Thermia Heat Pump Integration, you need to add the following to your `configuration.yaml` file:

```yaml
water_heater:
  - platform: thermia
    username: "your_thermia_username"
    password: "your_thermia_password"
```

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

## Contributions are welcome!
