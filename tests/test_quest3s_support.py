import sys
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.quest3 import models

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "xrbench"))
from xrbench import plan, sweep


class Quest3sSupportTests(unittest.TestCase):
    def test_quest3_family_includes_quest3s(self):
        self.assertTrue(models.is_quest3_family("Quest 3S"))
        models.require_quest3_family("Quest 3S", "test helper")

    def test_quest3_only_features_reject_quest3s(self):
        with self.assertRaises(RuntimeError):
            models.require_quest3_only("Quest 3S", "refresh scaling")

    def test_ncm_transport_is_valid_in_plan(self):
        plan.validate([plan.Segment("NCM", "alvr", transport="ncm")])

    def test_ncm_transport_falls_back_to_adb_with_reason(self):
        transport = sweep.Transport("192.168.1.5")
        logs = []
        with patch.object(transport, "_enter_ncm", side_effect=RuntimeError("no ncm adapter")), \
                patch.object(sweep, "adb"), \
                patch.object(sweep, "headset_ipv4", return_value=None), \
                patch.object(sweep.time, "sleep"), \
                patch.object(sweep, "log", side_effect=lambda m: logs.append(m)):
            transport._enter_ncm_with_fallback()
        self.assertEqual(transport.current, "adb")
        self.assertTrue(any("falling back to adb-forwarded TCP" in message for message in logs))


if __name__ == "__main__":
    unittest.main()
