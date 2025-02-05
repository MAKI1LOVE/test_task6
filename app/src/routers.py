from fastapi import APIRouter, Request

from src.scheduler_service import PeriodicSchedulerService, SchedulerService, scheduler
from src.schemas import Message

router = APIRouter()


@router.post("/create-message")
async def send_message(message: Message, request: Request):
    # TODO: cover with Manager
    if message.periodic and message.deferance:
        trigger = "interval"
        scheduler.add_job(
            PeriodicSchedulerService(request.app.state.rabbit).send_scheduled_message,
            trigger=trigger,
            args=[message],
            seconds=message.deferance,
        )
    else:
        scheduler.add_job(
            SchedulerService(request.app.state.rabbit).send_scheduled_message,
            args=[message],
        )

    return {"message": "Message scheduled for sending."}
