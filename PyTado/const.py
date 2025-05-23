"""Constant values for the Tado component."""

# API client ID
CLIENT_ID_DEVICE = "1bb50063-6b0c-4d11-bd99-387f4a91cc46"  # nosec B105

# Types
TYPE_AIR_CONDITIONING = "AIR_CONDITIONING"
TYPE_HEATING = "HEATING"
TYPE_HOT_WATER = "HOT_WATER"

# Base modes
CONST_MODE_OFF = "OFF"
CONST_MODE_SMART_SCHEDULE = "SMART_SCHEDULE"  # Use the schedule
CONST_MODE_AUTO = "AUTO"
CONST_MODE_COOL = "COOL"
CONST_MODE_HEAT = "HEAT"
CONST_MODE_DRY = "DRY"
CONST_MODE_FAN = "FAN"

CONST_LINK_OFFLINE = "OFFLINE"
CONST_CONNECTION_OFFLINE = "OFFLINE"

CONST_FAN_OFF = "OFF"
CONST_FAN_AUTO = "AUTO"
CONST_FAN_LOW = "LOW"
CONST_FAN_MIDDLE = "MIDDLE"
CONST_FAN_HIGH = "HIGH"

CONST_FAN_SPEED_OFF = "OFF"
CONST_FAN_SPEED_AUTO = "AUTO"
CONST_FAN_SPEED_SILENT = "SILENT"
CONST_FAN_SPEED_LEVEL1 = "LEVEL1"
CONST_FAN_SPEED_LEVEL2 = "LEVEL1"
CONST_FAN_SPEED_LEVEL3 = "LEVEL3"
CONST_FAN_SPEED_LEVEL4 = "LEVEL4"

CONST_VERTICAL_SWING_OFF = "OFF"
CONST_VERTICAL_SWING_ON = "ON"

CONST_HORIZONTAL_SWING_OFF = "OFF"
CONST_HORIZONTAL_SWING_ON = "ON"
CONST_HORIZONTAL_SWING_LEFT = "LEFT"
CONST_HORIZONTAL_SWING_MID_LEFT = "MID_LEFT"
CONST_HORIZONTAL_SWING_MID = "MID"
CONST_HORIZONTAL_SWING_MID_RIGHT = "MID_RIGHT"
CONST_HORIZONTAL_SWING_RIGHT = "RIGHT"

# When we change the temperature setting, we need an overlay mode
CONST_OVERLAY_TADO_MODE = "NEXT_TIME_BLOCK"  # wait until tado changes the mode automatic
CONST_OVERLAY_MANUAL = "MANUAL"  # the user has changed the temperature or mode manually
CONST_OVERLAY_TIMER = "TIMER"  # the temperature will be reset after a timespan

# Heat always comes first since we get the
# min and max tempatures for the zone from
# it.
# Heat is preferred as it generally has a lower minimum temperature
ORDERED_KNOWN_TADO_MODES = [
    CONST_MODE_HEAT,
    CONST_MODE_COOL,
    CONST_MODE_AUTO,
    CONST_MODE_DRY,
    CONST_MODE_FAN,
]

CONST_HVAC_HEAT = "HEATING"
CONST_HVAC_DRY = "DRYING"
CONST_HVAC_FAN = "FAN"
CONST_HVAC_COOL = "COOLING"
CONST_HVAC_IDLE = "IDLE"
CONST_HVAC_OFF = "OFF"
CONST_HVAC_HOT_WATER = TYPE_HOT_WATER

TADO_MODES_TO_HVAC_ACTION = {
    CONST_MODE_HEAT: CONST_HVAC_HEAT,
    CONST_MODE_DRY: CONST_HVAC_DRY,
    CONST_MODE_FAN: CONST_HVAC_FAN,
    CONST_MODE_COOL: CONST_HVAC_COOL,
}

TADO_HVAC_ACTION_TO_MODES = {
    CONST_HVAC_HEAT: CONST_MODE_HEAT,
    CONST_HVAC_HOT_WATER: CONST_HVAC_HEAT,
    CONST_HVAC_DRY: CONST_MODE_DRY,
    CONST_HVAC_FAN: CONST_MODE_FAN,
    CONST_HVAC_COOL: CONST_MODE_COOL,
}

# These modes will not allow a temp to be set
TADO_MODES_WITH_NO_TEMP_SETTING = [
    CONST_MODE_AUTO,
    CONST_MODE_DRY,
    CONST_MODE_FAN,
]

DEFAULT_TADO_PRECISION = 0.1
DEFAULT_TADOX_PRECISION = 0.01

HOME_DOMAIN = "homes"
DEVICE_DOMAIN = "devices"
