#pragma once

#include "esphome/core/component.h"
#include "esphome/core/defines.h"
#include "esphome/core/application.h"
#include "esphome/components/uart/uart.h"
#include "esphome/components/sensor/sensor.h"

#include <vector>

namespace esphome {
namespace weather_xm {

class WeatherXM : public Component, public uart::UARTDevice {

 public:
  WeatherXM();

  void set_battery_voltage_sensor(sensor::Sensor *sensor) { battery_voltage_sensor_ = sensor; }
  void set_humidity_sensor(sensor::Sensor *sensor) { humidity_sensor_ = sensor; }
  void set_illuminance_sensor(sensor::Sensor *sensor) { illuminance_sensor_ = sensor; }
  void set_precipitation_accumulated_sensor(sensor::Sensor *sensor) { precipitation_accumulated_sensor_ = sensor; }
  void set_precipitation_rate_sensor(sensor::Sensor *sensor) { precipitation_rate_sensor_ = sensor; }
  void set_pressure_sensor(sensor::Sensor *sensor) { pressure_sensor_ = sensor; }
  void set_temperature_sensor(sensor::Sensor *sensor) { temperature_sensor_ = sensor; }
  void set_uv_sensor(sensor::Sensor *sensor) { uv_sensor_ = sensor; }
  void set_uv_index_sensor(sensor::Sensor *sensor) { uv_index_sensor_ = sensor; }
  void set_wind_speed_sensor(sensor::Sensor *sensor) { wind_speed_sensor_ = sensor; }
  void set_wind_direction_sensor(sensor::Sensor *sensor) { wind_direction_sensor_ = sensor; }

  float get_setup_priority() const override { return setup_priority::DATA; }
  void setup() override;
  void loop() override;
  void dump_config() override;

 private:
  void update_sensor_(JsonObject values, sensor::Sensor *sensor, std::string node);
  sensor::Sensor *battery_voltage_sensor_{nullptr};
  sensor::Sensor *humidity_sensor_{nullptr};
  sensor::Sensor *illuminance_sensor_{nullptr};
  sensor::Sensor *precipitation_accumulated_sensor_{nullptr};
  sensor::Sensor *precipitation_rate_sensor_{nullptr};
  sensor::Sensor *pressure_sensor_{nullptr};
  sensor::Sensor *temperature_sensor_{nullptr};
  sensor::Sensor *uv_sensor_{nullptr};
  sensor::Sensor *uv_index_sensor_{nullptr};
  sensor::Sensor *wind_speed_sensor_{nullptr};
  sensor::Sensor *wind_direction_sensor_{nullptr};

  std::vector<uint8_t> rx_buffer_;
};

}  // namespace weather_xm
}  // namespace esphome
