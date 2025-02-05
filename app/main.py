from contextlib import asynccontextmanager

import aio_pika
from aio_pika.abc import AbstractConnection
from fastapi import FastAPI
from src.routers import router
from src.scheduler_service import scheduler
from src.settings import app_settings


async def connect_to_rabbitmq() -> AbstractConnection:
    connection = await aio_pika.connect_robust(app_settings.rabbit_settings.RABBIT_URL)
    channel = await connection.channel()
    exchange = await channel.declare_exchange(
        app_settings.rabbit_settings.RABBIT_QUEUE, aio_pika.ExchangeType.DIRECT
    )
    queue = await channel.declare_queue(app_settings.rabbit_settings.RABBIT_QUEUE)
    await queue.bind(exchange, app_settings.rabbit_settings.RABBIT_QUEUE)
    return connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbit = await connect_to_rabbitmq()
    scheduler.start()
    yield
    scheduler.shutdown()
    await app.state.rabbit.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
