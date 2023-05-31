from handlers.participant import third_nomination, first_notifications, first_nomination, second_notifications, \
    second_nomination, third_notifications
import asyncio
from handlers.referee import notifications_referee, nomination_referee
from datetime import datetime


async def run_task():
    print(f"Scheduler run at {datetime.now()}")
    while True:
        now = datetime.now()
        if now.month == 5 and now.day == 22 and now.hour == 10 and now.minute == 00:
            await first_notifications.first_notification()
            await notifications_referee.may_22()
        if now.month == 5 and now.day == 26 and now.hour == 10 and now.minute == 00:
            await first_notifications.second_notification()
            await notifications_referee.may_26()
        if now.month == 5 and now.day == 28 and now.hour == 10 and now.minute == 00:
            await first_notifications.third_notification()
            await notifications_referee.may_28()
        if now.month == 5 and now.day == 29 and now.hour == 9 and now.minute == 00:
            await first_notifications.fourth_notification()
            await notifications_referee.may_29()
        if now.month == 5 and now.day == 29 and now.hour == 9 and now.minute == 30:
            await first_nomination.start_nomination()
        if now.month == 5 and now.day == 30 and now.hour == 10 and now.minute == 00:
            await notifications_referee.may_30()
        if now.month == 5 and now.day == 31 and now.hour == 10 and now.minute == 00:
            await second_notifications.fifth_notification()
        if now.month == 6 and now.day == 1 and now.hour == 9 and now.minute == 00:
            await second_notifications.sixth_notification()
            await notifications_referee.june_1()
        if now.month == 6 and now.day == 1 and now.hour == 9 and now.minute == 30:
            await second_nomination.start_nomination()
        if now.month == 6 and now.day == 2 and now.hour == 10 and now.minute == 00:
            await notifications_referee.june_2()
        if now.month == 6 and now.day == 3 and now.hour == 10 and now.minute == 00:
            await third_notifications.fifth_notification()
        if now.month == 6 and now.day == 4 and now.hour == 9 and now.minute == 00:
            await third_notifications.sixth_notification()
            await notifications_referee.june_4()
        if now.month == 6 and now.day == 4 and now.hour == 9 and now.minute == 30:
            await third_nomination.start_nomination()
        if now.month == 6 and now.day == 5 and now.hour == 9 and now.minute == 30:
            await notifications_referee.june_5()

        await asyncio.sleep(60 - now.second)


if __name__ == '__main__':
    asyncio.run(run_task())
