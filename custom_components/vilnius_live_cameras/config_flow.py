"""Config flow for Vilnius Live Cameras."""

from homeassistant import config_entries

from .const import DOMAIN


class VilniusLiveCamerasConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the single, no-options setup flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create the integration entry."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="Vilnius Live Cameras", data={})
        return self.async_show_form(step_id="user")

