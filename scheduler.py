from handlers.participant import third_notifications
import asyncio
from datetime import datetime


async def run_task():
    print(f"Scheduler run at {datetime.now()}")
    while True:
        now = datetime.now()
        if now.month == 6 and now.day == 12 and now.hour == 19 and now.minute == 00:
            await third_notifications.result_notification()
        await asyncio.sleep(60 - now.second)


if __name__ == '__main__':
    asyncio.run(run_task())
