# ESPHome 2026.9.0 migration

ENVIRO-A1 uses an ESP32 revision 1.0 and an SHT31D, with no display.
Do not copy ENVIRO-B2's minimum_chip_revision 3.1 setting: that firmware cannot
boot on this older chip. Leave sram1_as_iram disabled until boot logs confirm
bootloader support. Preserve the existing API key and calibration settings.

## Install in two stages when upgrading older firmware

1. Install ESPHome 2026.9.0 on the build host.
2. In a local copy of this YAML, replace OTA `encryption: {}` with
   `password: !secret enviro_a1_api_key`. Compile and upload that transitional
   configuration using the existing device credentials.
3. Confirm the device boots, reconnects to Home Assistant, reports SHT31D readings,
   and logs `Encryption: offered, plaintext accepted`.
4. Restore `encryption: {}` and remove the OTA password. Compile and upload again
   using ESPHome 2026.9.0. Confirm `Encryption: required` and successful readings.
5. Verify another encrypted OTA upload succeeds before declaring migration complete.

Password and required encryption are mutually exclusive. The first upload to old
firmware is not encrypted. Do not enable required encryption in the upload config
before the running firmware supports it. USB flashing is an alternative.

For rollback, retain encrypted OTA and the unchanged API key while reverting
application changes, using ESPHome 2026.9.0. No device flashing is performed by
the validation script. Compile success does not establish hardware compatibility.

Source: https://esphome.io/components/ota/esphome/

## Development validation

Install `esphome==2026.9.0`, then run `python scripts/validate_config.py` for a full
compile, or add `--generate-only` for schema validation and C++ generation.
Validation copies only the YAML into a temporary directory with dummy credentials.
