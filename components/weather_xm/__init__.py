from esphome.components import binary_sensor, sensor
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import (
    CONF_ID,
    CONF_BATTERY_VOLTAGE,
    CONF_HUMIDITY,
    CONF_ILLUMINANCE,
    CONF_PRESSURE,
    CONF_TEMPERATURE,
    CONF_WIND_DIRECTION_DEGREES,
    CONF_WIND_SPEED,
    DEVICE_CLASS_EMPTY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_IRRADIANCE,
    DEVICE_CLASS_PRECIPITATION,
    DEVICE_CLASS_PRECIPITATION_INTENSITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    ENTITY_CATEGORY_DIAGNOSTIC,
    ICON_BRIGHTNESS_5,
    ICON_SIGN_DIRECTION,
    ICON_WEATHER_WINDY,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_CELSIUS,
    UNIT_DEGREES,
    UNIT_HECTOPASCAL,
    UNIT_KILOMETER_PER_HOUR,
    UNIT_LUX,
    UNIT_MILLIMETER,
    UNIT_MILLIVOLT,
    UNIT_PERCENT,
)

CONF_PRECIPITATION_RATE = "precipitation_rate"
CONF_PRECIPITATION_ACCUMULATED = "precipitation_accumulated"
CONF_UV = "uv"
CONF_UV_INDEX = "uv_index"
UNIT_COUNTS = "#"
UNIT_MILLIMETERS_PER_HOUR = "mm/h"
UNIT_UVI = "UVI"

CODEOWNERS = ["@RoganDawes"]

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["binary_sensor", "button", "sensor", "switch", "text_sensor"]

weather_xm_ns = cg.esphome_ns.namespace("weather_xm")
WeatherXM = weather_xm_ns.class_("WeatherXM", cg.Component, uart.UARTDevice)

CONF_WEATHER_XM_ID = "weather_xm_id"
CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(WeatherXM),
            cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_CELSIUS,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_TEMPERATURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
                unit_of_measurement=UNIT_PERCENT,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_HUMIDITY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_WIND_SPEED): sensor.sensor_schema(
                unit_of_measurement=UNIT_KILOMETER_PER_HOUR,
                icon=ICON_WEATHER_WINDY,
                accuracy_decimals=1,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_WIND_DIRECTION_DEGREES): sensor.sensor_schema(
                unit_of_measurement=UNIT_DEGREES,
                icon=ICON_SIGN_DIRECTION,
                accuracy_decimals=1,
            ),
            cv.Optional(CONF_ILLUMINANCE): sensor.sensor_schema(
                unit_of_measurement=UNIT_LUX,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_ILLUMINANCE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_UV_INDEX): sensor.sensor_schema(
                unit_of_measurement=UNIT_UVI,
                icon=ICON_BRIGHTNESS_5,
                accuracy_decimals=5,
                device_class=DEVICE_CLASS_EMPTY,
            ),
            cv.Optional(CONF_UV): sensor.sensor_schema(
                unit_of_measurement=UNIT_COUNTS,
                icon=ICON_BRIGHTNESS_5,
                accuracy_decimals=1,
                device_class=DEVICE_CLASS_EMPTY,
            ),
            cv.Optional(CONF_PRESSURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_HECTOPASCAL,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PRESSURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_BATTERY_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_MILLIVOLT,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_VOLTAGE,
                state_class=STATE_CLASS_MEASUREMENT,
                entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
            ),
            cv.Optional(CONF_PRECIPITATION_ACCUMULATED): sensor.sensor_schema(
                unit_of_measurement=UNIT_MILLIMETER,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PRECIPITATION,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_PRECIPITATION_RATE): sensor.sensor_schema(
                unit_of_measurement=UNIT_MILLIMETERS_PER_HOUR,
                accuracy_decimals=2,
                device_class=DEVICE_CLASS_PRECIPITATION_INTENSITY,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA),
    cv.has_at_least_one_key(
        CONF_BATTERY_VOLTAGE,
        CONF_HUMIDITY,
        CONF_ILLUMINANCE,
        CONF_PRESSURE,
        CONF_TEMPERATURE,
        CONF_WIND_DIRECTION_DEGREES,
        CONF_WIND_SPEED,
        CONF_UV,
        CONF_UV_INDEX,
    ),
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if sensor_config := config.get(CONF_BATTERY_VOLTAGE):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_battery_voltage_sensor(sens))

    if sensor_config := config.get(CONF_HUMIDITY):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_humidity_sensor(sens))

    if sensor_config := config.get(CONF_ILLUMINANCE):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_illuminance_sensor(sens))

    if sensor_config := config.get(CONF_PRECIPITATION_ACCUMULATED):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_precipitation_accumulated_sensor(sens))

    if sensor_config := config.get(CONF_PRECIPITATION_RATE):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_precipitation_rate_sensor(sens))

    if sensor_config := config.get(CONF_PRESSURE):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_pressure_sensor(sens))

    if sensor_config := config.get(CONF_TEMPERATURE):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_temperature_sensor(sens))

    if sensor_config := config.get(CONF_UV):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_uv_sensor(sens))

    if sensor_config := config.get(CONF_UV_INDEX):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_uv_index_sensor(sens))

    if sensor_config := config.get(CONF_WIND_SPEED):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_wind_speed_sensor(sens))

    if sensor_config := config.get(CONF_WIND_DIRECTION_DEGREES):
        sens = await sensor.new_sensor(sensor_config)
        cg.add(var.set_wind_direction_sensor(sens))

