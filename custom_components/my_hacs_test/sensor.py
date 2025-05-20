from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
import datetime

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    name = entry.data["name"]
    async_add_entities([HACSTestSensor(name)])

class HACSTestSensor(SensorEntity):
    def __init__(self, name):
        self._attr_name = name
        self._attr_unique_id = f"hacs_test_sensor_{name.lower().replace(' ', '_')}"
        self._attr_native_value = datetime.datetime.now().strftime("%H:%M:%S")

    async def async_update(self):
        self._attr_native_value = datetime.datetime.now().strftime("%H:%M:%S")