import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

class ChinaUnicomDataConfigFlow(config_entries.ConfigFlow, domain="unicom_bill_info"):
    """Config flow for China Unicom Data."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # You might want to add some basic validation here
            if not user_input["openid"]:
                errors["base"] = "openid_required"
            else:
                return self.async_create_entry(title=user_input["name"], data=user_input)

        data_schema = vol.Schema({
            vol.Required("name", default="联通数据"): str,
            vol.Required("openid"): str,
            vol.Required("refresh_interval", default=15): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=60)
            ),
            vol.Optional("create_individual_sensors", default=False): bool,
        })
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @callback
    @classmethod # 新增此行
    def async_get_options_flow(cls, config_entry): # 将 self 改为 cls
        """Get the options flow for this handler."""
        return ChinaUnicomDataOptionsFlow(config_entry)


class ChinaUnicomDataOptionsFlow(config_entries.OptionsFlow):
    """Options flow for China Unicom Data."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Required("name", default=self.config_entry.data.get("name", "联通数据")): str,
            vol.Required("openid", default=self.config_entry.data.get("openid")): str,
            vol.Required("refresh_interval", default=self.config_entry.data.get("refresh_interval", 15)): vol.All(
                vol.Coerce(int), vol.Range(min=1, max=60)
            ),
            vol.Optional("create_individual_sensors", default=self.config_entry.data.get("create_individual_sensors", False)): bool,
        })
        return self.async_show_form(step_id="init", data_schema=options_schema)