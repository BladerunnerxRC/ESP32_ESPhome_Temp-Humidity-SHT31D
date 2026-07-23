<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>

  <h1>ENVIRO-A1 ESPHome Configuration</h1>
  <p>
    This repository holds the ESPHome YAML for the ENVIRO-A1 ESP32 board—an environmental monitor with live-tunable temperature, humidity, uptime, and Wi-Fi diagnostics, complete with connectivity safety logic and Home Assistant integration.
  </p>
# Confirmed to work with ESPHome v2026.4.2

[Changelog](https://esphome.io/changelog/)

  <hr />

  <h2>📑 Table of Contents</h2>
  <ul>
    <li><a href="#gpio-pin-assignments">GPIO Pin Assignments</a></li>
    <li><a href="#substitutions">Substitutions</a></li>
    <li><a href="#esphome--esp32-settings">ESPHome &amp; ESP32 Settings</a></li>
    <li><a href="#i²c-bus">I²C Bus</a></li>
    <li><a href="#logger">Logger</a></li>
    <li><a href="#api--ota">API &amp; OTA</a></li>
    <li><a href="#time">Time</a></li>
    <li><a href="#wi-fi-configuration">Wi-Fi Configuration</a></li>
    <li><a href="#sensors">Sensors</a></li>
    <li><a href="#binary-sensors">Binary Sensors</a></li>
    <li><a href="#switches">Switches</a></li>
    <li><a href="#buttons">Buttons</a></li>
    <li><a href="#number-inputs">Number Inputs</a></li>
  </ul>

  <hr />

  <h2 id="gpio-pin-assignments">🔌 GPIO Pin Assignments</h2>
  <table>
    <thead>
      <tr><th>Function</th><th>GPIO Pin</th><th>Notes</th></tr>
    </thead>
    <tbody>
      <tr><td>I²C SDA</td><td>21</td><td>Data line for I²C bus</td></tr>
      <tr><td>I²C SCL</td><td>22</td><td>Clock line for I²C bus</td></tr>
      <tr><td>Onboard LED (Wi-Fi LED)</td><td>2</td><td>Status LED; active LOW</td></tr>
    </tbody>
  </table>

  <hr />

  <h2 id="substitutions">🔧 Substitutions</h2>
  <ul>
    <li><code>temperature_calibration</code> – default calibration offset in °C</li>
    <li><code>humidity_calibration</code> – default calibration offset in %</li>
    <li><code>update_interval_s</code> – default sensor polling interval (seconds)</li>
    <li><code>update_interval_wifi</code> – default Wi-Fi signal update interval (seconds)</li>
  </ul>
  <p>These are compile-time defaults only; the live values come from the Number entities below, which persist across reboots.</p>

  <hr />

  <h2 id="esphome--esp32-settings">⚙️ ESPHome &amp; ESP32 Settings</h2>
  <ul>
    <li><strong>Device Identity</strong>: name = <code>enviro-a1</code>, friendly_name = <code>ENVIRO-A1</code></li>
    <li><strong>Boot Hook</strong>: priority −100; re-applies the restored update intervals to the sensor pollers</li>
    <li><strong>ESP32 Board</strong>: <code>esp32dev</code>, framework = esp-idf</li>
  </ul>

  <hr />

  <h2 id="i²c-bus">🔗 I²C Bus</h2>
  <ul>
    <li><code>id</code>: bus_a</li>
    <li><code>sda</code>: GPIO21</li>
    <li><code>scl</code>: GPIO22</li>
    <li><code>scan</code>: true</li>
  </ul>
  <p>Enables automatic scanning of connected I²C devices.</p>

  <hr />

  <h2 id="logger">📝 Logger</h2>
  <ul>
    <li><code>level</code>: DEBUG (ERROR, WARN, INFO, DEBUG, VERY_VERBOSE)</li>
    <li><code>baud_rate</code>: 115200 (0 to disable)</li>
  </ul>
  <p>Provides granular runtime diagnostics.</p>

  <hr />

  <h2 id="api--ota">🔒 API &amp; OTA</h2>
  <ul>
    <li><strong>API</strong>: encrypted key via <code>!secret enviro_a1_api_key</code></li>
    <li><strong>OTA</strong>: platform = esphome, password = same encrypted key</li>
    <li><strong>Safe Mode</strong>: enabled so the device stays OTA-reachable after repeated boot failures</li>
  </ul>

  <hr />

  <h2 id="time">⏰ Time</h2>
  <p>Uses Home Assistant as time source (<code>id: ha_time</code>) for accurate timestamps.</p>

  <hr />

  <h2 id="wi-fi-configuration">📶 Wi-Fi Configuration</h2>
  <ul>
    <li>Credentials from secrets, <code>power_save_mode: none</code>, <code>output_power: 15.5 dB</code></li>
    <li>Static IP: 10.100.50.16 / Gateway: 10.100.50.1 / Subnet: 255.255.255.0</li>
    <li>DNS: 8.8.8.8, 8.8.4.4</li>
    <li><strong>on_connect</strong>: turns on LED, logs “WiFi connected,” fires HA notification</li>
    <li><strong>on_disconnect</strong>: turns off LED, logs, waits 30 s, then conditionally restarts</li>
    <li><strong>Fallback AP</strong>: SSID/password from secrets, with <code>captive_portal</code> enabled for recovery setup</li>
  </ul>

  <hr />

  <h2 id="sensors">🌡 Sensors</h2>
  <ul>
    <li><strong>Wi-Fi Signal</strong> (<code>wifi_signal_sensor</code>) – RSSI every <code>${update_interval_wifi}</code></li>
    <li><strong>SHT31D Temp &amp; Humidity</strong> (<code>sht31d_component</code>)
      <ul>
        <li>I²C @ 0x44 on <code>bus_a</code>, internal heater disabled</li>
        <li>Lambda filters add the calibration Number values to each reading</li>
        <li>Interval <code>${update_interval_s}</code> seconds, adjustable at runtime</li>
      </ul>
    </li>
    <li><strong>Uptime</strong> (<code>enviro_a1_uptime_sensor</code>) – seconds since boot</li>
  </ul>

  <hr />

  <h2 id="binary-sensors">⚙️ Binary Sensors</h2>
  <ul>
    <li><strong>Connection Status</strong> (<code>connection_status</code>) – device health</li>
    <li><strong>Reboot Trigger</strong> (<code>reboot_trigger</code>) – tied to HA <code>input_boolean.reboot_enviro_a1</code> (debounced 60 s)</li>
  </ul>

  <hr />

  <h2 id="switches">🔀 Switches</h2>
  <ul>
    <li><strong>Wi-Fi Connect LED</strong> (<code>onboard_led</code>) – GPIO2</li>
    <li><strong>Reboot_ENVIRO-A1</strong> (<code>reboot_enviro_a1_restart</code>) – virtual restart switch</li>
  </ul>

  <hr />

  <h2 id="buttons">🔘 Buttons</h2>
  <ul>
    <li><strong>Refresh Sensors</strong> (<code>refresh_sensors</code>) – immediately updates SHT31D, Wi-Fi signal, and uptime</li>
  </ul>

  <hr />

  <h2 id="number-inputs">🔢 Number Inputs</h2>
  <ul>
    <li><strong>Temperature Calibration</strong> (−10…+10 °C, step 0.1) – applied by the temperature filter; triggers an immediate refresh</li>
    <li><strong>Humidity Calibration</strong> (−10…+10 %, step 0.1) – applied by the humidity filter; triggers an immediate refresh</li>
    <li><strong>Update Interval</strong> (10–3600 s, step 1) – reschedules the SHT31D poller immediately</li>
    <li><strong>Wi-Fi Update Interval</strong> (10–3600 s, step 1) – reschedules the Wi-Fi signal poller immediately</li>
  </ul>
  <p>All four persist across reboots via <code>restore_value</code>; the intervals are re-applied by the boot hook.</p>

  <hr />

  <p>
    With this structure, you can quickly navigate and customize every aspect of the ENVIRO-A1 ESPHome setup in GitHub’s README view.
  </p>

</body>
</html>
