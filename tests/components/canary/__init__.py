"""Tests for the canary component."""
from typing import Optional
from unittest.mock import MagicMock, PropertyMock

from canary.api import SensorType

from homeassistant.components.canary.const import DOMAIN
from homeassistant.const import CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME
from homeassistant.helpers.typing import HomeAssistantType
from tests.common import MockConfigEntry

ENTRY_CONFIG = {
    CONF_PASSWORD: "test-password",
    CONF_USERNAME: "test-username",
    CONF_TIMEOUT: 1,
}

YAML_CONFIG = {
    CONF_PASSWORD: "test-password",
    CONF_USERNAME: "test-username",
}


async def init_integration(
    hass: HomeAssistantType,
    *,
    data: dict = ENTRY_CONFIG,
    options: Optional[dict] = None,
    skip_entry_setup: bool = False,
) -> MockConfigEntry:
    """Set up the Canary integration in Home Assistant."""
    entry = MockConfigEntry(domain=DOMAIN, data=data, options=options)
    entry.add_to_hass(hass)

    if not skip_entry_setup:
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    return entry


def mock_device(device_id, name, is_online=True, device_type_name=None):
    """Mock Canary Device class."""
    device = MagicMock()
    type(device).device_id = PropertyMock(return_value=device_id)
    type(device).name = PropertyMock(return_value=name)
    type(device).is_online = PropertyMock(return_value=is_online)
    type(device).device_type = PropertyMock(
        return_value={"id": 1, "name": device_type_name}
    )
    return device


def mock_location(
    location_id, name, is_celsius=True, devices=None, mode=None, is_private=False
):
    """Mock Canary Location class."""
    location = MagicMock()
    type(location).location_id = PropertyMock(return_value=location_id)
    type(location).name = PropertyMock(return_value=name)
    type(location).is_celsius = PropertyMock(return_value=is_celsius)
    type(location).is_private = PropertyMock(return_value=is_private)
    type(location).devices = PropertyMock(return_value=devices or [])
    type(location).mode = PropertyMock(return_value=mode)
    return location


def mock_mode(mode_id, name):
    """Mock Canary Mode class."""
    mode = MagicMock()
    type(mode).mode_id = PropertyMock(return_value=mode_id)
    type(mode).name = PropertyMock(return_value=name)
    type(mode).resource_url = PropertyMock(return_value=f"/v1/modes/{mode_id}")
    return mode


def mock_reading(sensor_type, sensor_value):
    """Mock Canary Reading class."""
    reading = MagicMock()
    type(reading).sensor_type = SensorType(sensor_type)
    type(reading).value = PropertyMock(return_value=sensor_value)
    return reading
