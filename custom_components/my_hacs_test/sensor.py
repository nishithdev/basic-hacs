from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import datetime

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([HACSTestSensor()])

class HACSTestSensor(SensorEntity):
    def __init__(self):
        self._attr_name = "HACS Test Sensor"
        self._attr_unique_id = "hacs_test_sensor"

    @property
    def native_value(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    @property
    def native_unit_of_measurement(self):
        return None

    async def async_update(self):
        # Called by HA scheduler
        self._attr_native_value = datetime.datetime.now().strftime("%H:%M:%S")