"""
Tests for DeviceOptimizer engine.
"""

from unittest.mock import MagicMock
from phone_fix.engine.optimizer import DeviceOptimizer

def test_trim_caches(mock_adb):
    opt = DeviceOptimizer(mock_adb)
    res = opt.trim_caches(20)
    assert res is True
    mock_adb.shell.assert_called_with("pm trim-caches 20G")

def test_disable_bloatware(mock_adb):
    opt = DeviceOptimizer(mock_adb)
    mock_adb.run_raw.return_value = ("Success", "", 0)

    disabled, failed = opt.disable_bloatware(["com.miui.msa.global"])
    assert "com.miui.msa.global" in disabled
    assert len(failed) == 0

def test_rollback_packages(mock_adb):
    opt = DeviceOptimizer(mock_adb)
    mock_adb.run_raw.return_value = ("Package installed", "", 0)

    restored = opt.rollback_packages(["com.miui.msa.global"])
    assert "com.miui.msa.global" in restored

def test_unlock_refresh_rate(mock_adb):
    opt = DeviceOptimizer(mock_adb)
    res = opt.unlock_refresh_rate(120)
    assert res is True
    mock_adb.shell.assert_any_call("settings put system peak_refresh_rate 120")

def test_aot_compilation(mock_adb):
    opt = DeviceOptimizer(mock_adb)
    mock_adb.shell.return_value = "Success"
    compiled = opt.compile_apps_aot(["com.miui.home"])
    assert "com.miui.home" in compiled
