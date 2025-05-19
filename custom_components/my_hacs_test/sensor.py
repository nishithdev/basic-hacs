from homeassistant.helpers.entity import Entity

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([MyTestSensor()])

class MyTestSensor(Entity):
    def __init__(self):
        self._state = "Hello from HACS"

    @property
    def name(self):
        return "HACS Test Sensor"

    @property
    def state(self):
        return self._state