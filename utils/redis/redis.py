from typing import Optional

import asyncio

import aioredis

from dataclasses import dataclass

# local imports
from data import config


@dataclass
class Redis:
    ip: str = config.REDIS['ip']
    port: int = config.REDIS['port']
    _redis: Optional[aioredis.Redis] = None

    @property
    async def client(self) -> aioredis.Redis:
        if self.closed:
            if not self._redis:
                try:
                    await self.connect()
                except asyncio.TimeoutError:
                    raise TimeoutError('Redis connection timeout')
                else:
                    return self._redis
            else:
                raise RuntimeError("Redis connection is not opened")
        return self._redis

    @property
    def closed(self):
        return not self._redis or self._redis.closed

    async def connect(self):
        if self.closed:
            self._redis = await aioredis.create_redis_pool(self.ip, timeout=10, encoding='utf8')

    async def disconnect(self):
        if not self.closed:
            self._redis.close()
            await self._redis.wait_closed()
