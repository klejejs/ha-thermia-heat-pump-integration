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
## Manually installing Python Thermia Online API

Ordinarily Home Assistant will automatically install dependencies such as the [Python Thermia Online API](https://github.com/klejejs/python-thermia-online-api) when installing an integration. However if you are working on improving this integration, it may be helpful to install a forked version of the [Python Thermia Online API](https://github.com/klejejs/python-thermia-online-api) with improvements you may be working on. The easiest way to do this, is to push your changes to a fork of [Python Thermia Online API](https://github.com/klejejs/python-thermia-online-api) on your github.

Then if you have manually installed Home Assistant, you can install the forked Thermia Online API as follows:

```shell
root@ha:~$ pip uninstall -y ThermiaOnlineAPI
root@ha:~$ pip install git+https://github.com/<username>/python-thermia-online-api.git#egg=ThermiaOnlineAPI
```

Otherwise if you are using the [Home Assistant Virtual Machine](https://www.home-assistant.io/installation/alternative), you will first need to logon to the docker container where Home Assistant is running before following the steps above.

```shell
root@ha:~$ docker exec -it homeassistant sh
/config # pip uninstall -y ThermiaOnlineAPI
/config # pip install git+https://github.com/<username>/python-thermia-online-api.git#egg=ThermiaOnlineAPI
...
```


---

## Contributions are welcome!
