from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class MyHACSTestConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Future: Validate user_id and password with CoServ API
            return self.async_create_entry(
                title=user_input["user_id"],
                data={
                    "user_id": user_input["user_id"],
                    "password": user_input["password"]
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("user_id"): str,
                vol.Required("password"): str,
            }),
            errors=errors
        )