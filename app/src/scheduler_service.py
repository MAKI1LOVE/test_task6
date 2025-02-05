import asyncio

import aio_pika
from aio_pika.abc import AbstractConnection
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.schemas import Message
from src.settings import app_settings

scheduler = AsyncIOScheduler()


class SchedulerService:
    def __init__(self, connection: AbstractConnection):
        self._rabbit_connection = connection
        self._scheduler = scheduler

    async def _prepare_connection(self):
        self._channel = await self._rabbit_connection.channel()
        self._exchange = await self._channel.get_exchange(
            app_settings.rabbit_settings.RABBIT_QUEUE
        )

    async def _close_connection(self):
        await self._channel.close()

    async def send_scheduled_message(self, message: Message):
        await self._prepare_connection()
        await asyncio.sleep(message.deferance)
        await self._send_message(message.text)
        await self._close_connection()

    async def _send_message(self, text: str):
        await self._exchange.publish(
            aio_pika.Message(body=text.encode()),
            routing_key=app_settings.rabbit_settings.RABBIT_QUEUE,
        )
        print(f"Sent scheduled message: {text}")


class PeriodicSchedulerService(SchedulerService):
    async def send_scheduled_message(self, message: Message):
        await self._prepare_connection()
        await self._send_message(message.text)
        await self._prepare_connection()
