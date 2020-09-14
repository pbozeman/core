"""The tests for the Canary component."""
from requests import ConnectTimeout

from homeassistant.components.canary import DOMAIN
from homeassistant.config_entries import (
    ENTRY_STATE_LOADED,
    ENTRY_STATE_NOT_LOADED,
    ENTRY_STATE_SETUP_RETRY,
)
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.setup import async_setup_component
from tests.common import MockConfigEntry

from . import ENTRY_CONFIG, YAML_CONFIG, init_integration

from tests.async_mock import patch


async def test_import_from_yaml(hass, canary) -> None:
    """Test import from YAML."""
    with patch(
        "homeassistant.components.canary.async_setup_entry",
        return_value=True,
    ):
        assert await async_setup_component(hass, DOMAIN, {DOMAIN: YAML_CONFIG})
        await hass.async_block_till_done()

    entries = hass.config_entries.async_entries(DOMAIN)
    assert len(entries) == 1

    assert entries[0].data[CONF_USERNAME] == "test-username"
    assert entries[0].data[CONF_PASSWORD] == "test-password"


async def test_unload_entry(hass, canary):
    """Test successful unload of entry."""
    entry = await init_integration(hass)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert entry.state == ENTRY_STATE_LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state == ENTRY_STATE_NOT_LOADED
    assert not hass.data.get(DOMAIN)


async def test_async_setup_raises_entry_not_ready(hass, canary):
    """Test that it throws ConfigEntryNotReady when exception occurs during setup."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=ENTRY_CONFIG)
    config_entry.add_to_hass(hass)

    canary.side_effect = ConnectTimeout()

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state == ENTRY_STATE_SETUP_RETRY
