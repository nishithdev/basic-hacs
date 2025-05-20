from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
import httpx

AUTH_URL = "https://coserv.smarthub.coop/services/oauth/auth/v2"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    user_id = entry.data["user_id"]
    password = entry.data["password"]
    async_add_entities([CoServAccessTokenSensor(user_id, password)])


class CoServAccessTokenSensor(SensorEntity):
    def __init__(self, user_id: str, password: str):
        self._user_id = user_id
        self._password = password
        self._attr_name = "CoServ Access Token"
        self._attr_unique_id = f"coserv_access_token_sensor_{user_id}"
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        cookies = {
            "JSESSIONID-consumer_1.0": "placeholder",
            "XSRF-TOKEN": "placeholder",
        }

        data = {
            "userId": self._user_id,
            "password": self._password
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(AUTH_URL, headers=headers, cookies=cookies, data=data)
                
                if response.status_code == 200:
                    json_data = response.json()
                    token = json_data.get("access_token")
                    
                    if token:
                        self._attr_native_value = token
                        self._attr_extra_state_attributes = {
                            "expires_in": json_data.get("expires_in"),
                            "token_type": json_data.get("token_type"),
                            "status_code": response.status_code
                        }
                    else:
                        self._attr_native_value = "Login failed"
                        self._attr_extra_state_attributes = {
                            "error": "No access token in response",
                            "status_code": response.status_code,
                            "response_text": response.text
                        }

                else:
                    self._attr_native_value = f"HTTP error {response.status_code}"
                    self._attr_extra_state_attributes = {
                        "reason": response.reason_phrase,
                        "status_code": response.status_code,
                        "response_text": response.text
                    }

        except httpx.RequestError as e:
            self._attr_native_value = "Connection error"
            self._attr_extra_state_attributes = {
                "error": str(e)
            }

        except Exception as e:
            self._attr_native_value = "Unexpected error"
            self._attr_extra_state_attributes = {
                "error": str(e)
            }