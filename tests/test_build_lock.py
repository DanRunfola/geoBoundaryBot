import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from builder import run


class BuildLockTimestampTests(unittest.TestCase):
    def test_lease_spec_includes_microseconds_for_whole_seconds(self):
        now = datetime(2026, 9, 28, 16, 13, 7, tzinfo=timezone.utc)
        lock = run.BuildLock("test-lock", "default", "test-driver")

        with patch("builder.run._utcnow", return_value=now):
            spec = lock._spec(now)

        self.assertEqual(spec["acquireTime"], "2026-09-28T16:13:07.000000Z")
        self.assertEqual(spec["renewTime"], "2026-09-28T16:13:07.000000Z")

    def test_preserves_nonzero_microseconds(self):
        now = datetime(2026, 9, 28, 16, 13, 7, 123456, tzinfo=timezone.utc)
        self.assertEqual(run._k8s_time(now), "2026-09-28T16:13:07.123456Z")


if __name__ == "__main__":
    unittest.main()
