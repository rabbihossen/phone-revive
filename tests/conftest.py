"""
Shared pytest fixtures and mock outputs for PhoneFix tests.
"""

import pytest
from unittest.mock import MagicMock
from phone_fix.core.adb import AdbBridge, ConnectedDevice

MOCK_DEVICES_OUTPUT = """List of devices attached
8900bcb4               device usb:34668544X product:tapas_in model:23027RAD4I device:tapas transport_id:1
192.168.0.100:5555     device product:tapas_in model:23027RAD4I device:tapas transport_id:2
unauthorized_device    unauthorized transport_id:3
"""

MOCK_DF_OUTPUT = """Filesystem       Size Used Avail Use% Mounted on
/dev/block/dm-63  48G  33G   15G  69% /data/user/0
"""

MOCK_MEMINFO_OUTPUT = """MemTotal:        5774524 kB
MemFree:          186464 kB
MemAvailable:    2840736 kB
Buffers:           12340 kB
Cached:          1500000 kB
SwapTotal:       4194300 kB
SwapFree:        2970820 kB
"""

MOCK_BATTERY_OUTPUT = """Current Battery Service state:
  AC powered: true
  USB powered: false
  status: 2
  health: 2
  present: true
  level: 85
  scale: 100
  voltage: 4100
  temperature: 320
  technology: Li-poly
"""

MOCK_DISKSTATS_OUTPUT = """Data-Free: 15000000K / 50000000K total = 30% free
Package Names: ["com.android.chrome","com.facebook.katana"]
App Sizes: [150000000, 200000000]
App Data Sizes: [400000000, 500000000]
Cache Sizes: [100000000, 150000000]
"""

@pytest.fixture
def mock_adb():
    adb = MagicMock(spec=AdbBridge)
    adb.target_serial = "8900bcb4"
    adb.run_raw.return_value = (MOCK_DEVICES_OUTPUT, "", 0)
    adb.shell.return_value = ""
    adb.shell_safe.return_value = ""
    return adb
