# AllianceAuth Ravworks Exporter

This is a plugin for [AllianceAuth](https://gitlab.com/allianceauth/allianceauth) that exports ESI data to a config file for [Ravworks](https://ravworks.com/).

## Prerequisites

This plugin requires a working AllianceAuth installation with v3 as a minimum version. See the [AllianceAuth installation instructions](https://allianceauth.readthedocs.io/en/latest/installation/index.html) for more information.

Data from ESI are not directly fetched by this application, instead it relies on other AllianceAuth plugins. Currently the following plugins are supported:

Skills:

- [MemberAudit](https://apps.allianceauth.org/apps/detail/aa-memberaudit)
- [CorpTools](https://apps.allianceauth.org/apps/detail/allianceauth-corptools)

Structures:

- Work in progress

If there are multiple plugins for the same functionality, only 1 is needed. If no plugin is installed, that functionality will be unavailable.

## Installation

1. Install the package with pip:

    ```bash
    pip install aa-ravworks-exporter
    ```

2. Add `'ravworks_exporter',` to your `INSTALLED_APPS` in `local.py`

## Basic usage

1. Download the config file from Ravworks website. This apps doesn't directly create the config files but rather update existing ones with data from ESI.
2. Use it in the form in this plugin page on AllianceAuth.
3. Download the update config file and use it on Ravworks website.
