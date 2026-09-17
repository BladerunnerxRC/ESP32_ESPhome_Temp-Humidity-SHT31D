# SHT31D acceptance checks

The stale diagnostic is on until both sensors have published finite readings.
It turns on if either reading ages beyond three configured sampling intervals
plus five seconds (95 seconds at the default 30-second interval). Home Assistant
retains the last good readings; use the problem entity in alerts and automations.

After installing on the device:

1. Check temperature and humidity, then change each calibration number and verify
   the next measurement uses it. Verify humidity remains between 0 and 100%.
2. Interrupt the sensor connection safely. Check the stale diagnostic turns on
   after the deadline while the connection-status entity remains online.
3. Restore the sensor connection and verify fresh readings clear the diagnostic.
   If sensor initialization failed at boot, a device restart may be necessary.
4. Change the sampling interval, verify the new freshness deadline, then reboot
   and confirm both the interval and calibration values restore correctly.
5. Repeat Refresh Sensors and calibration changes while watching I2C logs.

These checks require the physical device and have not been performed by the
automated build. SHT31D measurement timing differs from DHT22; no DHT-specific
two-second cooldown or display code is introduced.
