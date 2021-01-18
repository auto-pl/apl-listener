import asyncio
import datetime
import unittest
from typing import Any, cast
from unittest import mock

import asyncpg

import apl_listener  # pylint: disable=import-error


class TestOffline(unittest.IsolatedAsyncioTestCase):
    """Test that can be performed without a database connection."""

    def setUp(self) -> None:
        """Run before every individual test case."""
        self._old_facility_converter = apl_listener._client._base_from_facility

        async def dummy(*args: Any) -> int:
            return 0

        apl_listener._client._base_from_facility = dummy

    def tearDown(self) -> None:
        """Run after every individual test case."""
        apl_listener._client._base_from_facility = self._old_facility_converter

    async def test_connect(self) -> None:
        """Test the event client instantiation and connection."""
        TIMEOUT = 5.0
        INTERVAL = 0.1
        pool = cast(asyncpg.pool.Pool, mock.MagicMock())
        listener = apl_listener.EventListener('s:example', pool)
        asyncio.get_running_loop().create_task(listener.connect())
        for _ in range(round(TIMEOUT/INTERVAL)):
            if listener._dispatch_cache:
                break
            await asyncio.sleep(INTERVAL)
        else:
            self.fail(f'No message received after {TIMEOUT} seconds')
        await listener.close()
        self.assertTrue(len(listener._dispatch_cache) >= 1)
        last_update = listener._dispatch_last_update
        time_since = last_update - datetime.datetime.now()
        self.assertLess(time_since.total_seconds(), TIMEOUT)
