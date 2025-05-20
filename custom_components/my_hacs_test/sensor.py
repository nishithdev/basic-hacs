from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    user_id = entry.data["user_id"]
    async_add_entities([CoServTestSensor(user_id)])

class CoServTestSensor(SensorEntity):
    def __init__(self, user_id):
        self._attr_name = "CoServ Login Sensor"
        self._attr_unique_id = f"coserv_login_sensor_{user_id.lower().replace('@', '_').replace('.', '_')}"
        self._attr_native_value = f"Configured for user ID: {user_id}"

    async def async_update(self):
        # This is where we'll later fetch data from CoServ
        pass