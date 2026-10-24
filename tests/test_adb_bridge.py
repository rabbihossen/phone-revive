"""
Tests for AdbBridge core class.
"""

import pytest
from unittest.mock import patch, MagicMock
from phone_fix.core.adb import AdbBridge, ConnectedDevice
from phone_fix.core.exceptions import DeviceNotFoundError, DeviceUnauthorizedError, CommandExecutionError
from tests.conftest import MOCK_DEVICES_OUTPUT

def test_list_devices_parsing():
    bridge = AdbBridge(adb_path="/usr/bin/adb")
    with patch.object(bridge, "run_raw", return_value=(MOCK_DEVICES_OUTPUT, "", 0)):
        devices = bridge.list_devices()
        assert len(devices) == 3
        assert devices[0].serial == "8900bcb4"
        assert devices[0].state == "device"
        assert devices[0].model == "23027RAD4I"
        assert devices[0].is_authorized is True

        assert devices[2].serial == "unauthorized_device"
        assert devices[2].state == "unauthorized"
        assert devices[2].is_authorized is False

def test_select_device_auto():
    bridge = AdbBridge(adb_path="/usr/bin/adb")
    with patch.object(bridge, "run_raw", return_value=(MOCK_DEVICES_OUTPUT, "", 0)):
        dev = bridge.select_device()
        assert dev.serial == "8900bcb4"
        assert bridge.target_serial == "8900bcb4"

def test_select_device_unauthorized_raises():
    bridge = AdbBridge(adb_path="/usr/bin/adb")
    unauth_out = "List of devices attached\ndev1  unauthorized\n"
    with patch.object(bridge, "run_raw", return_value=(unauth_out, "", 0)):
        with pytest.raises(DeviceUnauthorizedError):
            bridge.select_device()

def test_select_device_not_found():
    bridge = AdbBridge(adb_path="/usr/bin/adb")
    with patch.object(bridge, "run_raw", return_value=("List of devices attached\n", "", 0)):
        with pytest.raises(DeviceNotFoundError):
            bridge.select_device()

def test_shell_command_error_raises():
    bridge = AdbBridge(adb_path="/usr/bin/adb", target_serial="dev1")
    with patch.object(bridge, "run_raw", return_value=("", "Error occurred", 1)):
        with pytest.raises(CommandExecutionError):
            bridge.shell("some_failing_cmd")

def test_shell_safe_returns_default_on_error():
    bridge = AdbBridge(adb_path="/usr/bin/adb", target_serial="dev1")
    with patch.object(bridge, "run_raw", return_value=("", "Error", 1)):
        res = bridge.shell_safe("failing_cmd", default="fallback")
        assert res == "fallback"
