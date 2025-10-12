#include "weather_xm.h"
#include "esphome/core/log.h"
#include "esphome/core/util.h"
#include "esphome/core/helpers.h"
#include "esphome/components/json/json_util.h"

namespace esphome {
namespace weather_xm {

static const char *TAG = "weather_xm";

WeatherXM::WeatherXM() {}

void WeatherXM::setup() {
  rx_buffer_.reserve(2048);
}

void WeatherXM::dump_config() {
  ESP_LOGCONFIG(TAG, "WeatherXM");
  LOG_SENSOR("  ", "Temperature", temperature_sensor_);
}

void WeatherXM::update_sensor_(JsonObject values, sensor::Sensor *sensor, std::string node) {
  if (sensor != nullptr) {
    if (values[node].is<float>()) {
      float value = values[node];
      sensor->publish_state(value);
    }
  }
}

void WeatherXM::loop() {
  size_t a = available();
  if (a > 0) {
    std::vector<uint8_t> rx;
    rx.resize(a);
    if (read_array(rx.data(), a)) {
      rx_buffer_.insert(rx_buffer_.end(), std::begin(rx), std::begin(rx) + a);
    } else {
      ESP_LOGW(TAG, "Read from UART RX buffer failed");
      return;
    }
  }
  if (a > 0) {
    while (rx_buffer_.size() > 0) {
      int16_t res = json::try_find_json(rx_buffer_);
      if (res < 0) {
        std::string discard = std::string{ rx_buffer_.begin(), rx_buffer_.begin() - res };
        rx_buffer_.erase(rx_buffer_.begin(), rx_buffer_.begin()-res);
      } else if (res > 0) {
        if (res > 512) { // JSON object is at least this size
          std::string json = std::string{ rx_buffer_.begin(), rx_buffer_.begin() + res };
          ESP_LOGD(TAG, "Parsing %s",json.c_str());
          JsonDocument root = json::parse_json(rx_buffer_.data(), res);
          if (root.is<JsonArray>()) {
            for (auto entry : root.as<JsonArray>()) {
              if(entry["values"].is<JsonObject>()) {
                JsonObject values = entry["values"];
                update_sensor_(values, battery_voltage_sensor_, "ws_bat_mv");
                update_sensor_(values, humidity_sensor_, "humidity");
                update_sensor_(values, illuminance_sensor_, "illuminance");
                update_sensor_(values, precipitation_accumulated_sensor_, "precipitation_accumulated");
                update_sensor_(values, precipitation_rate_sensor_, "precipitation_rate");
                update_sensor_(values, pressure_sensor_, "pressure");
                update_sensor_(values, temperature_sensor_, "temperature");
                update_sensor_(values, uv_sensor_, "fo_uv");
                update_sensor_(values, uv_index_sensor_, "uv_index");
                update_sensor_(values, wind_speed_sensor_, "wind_speed");
                update_sensor_(values, wind_direction_sensor_, "wind_direction");
              }
            }
          }
        }
        rx_buffer_.erase(rx_buffer_.begin(), rx_buffer_.begin()+res);
      } else {
        break;
      }
    }
  }
}

}  // namespace weather_xm
}  // namespace esphome
