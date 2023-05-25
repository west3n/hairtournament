from aiogram import Dispatcher
import logging

from aiogram import types

from handlers.commands import register as reg_handlers
from handlers.registration import register as reg_registration
from handlers.participant.first_notifications import register as reg_participant_notifications
from handlers.participant.first_nomination import register as reg_participant_first_nomination
from handlers.participant.second_notifications import register as reg_participant_second_notifications
from handlers.participant.second_nomination import register as reg_participant_second_nomination
from handlers.participant.third_notifications import register as reg_participant_third_notifications
from handlers.participant.third_nomination import register as reg_participant_third_nomination
from handlers.participant.distrib import register as reg_participant_distib
from handlers.referee.nomination_referee import register as reg_nomination_referee
from handlers.referee.notifications_referee import register as reg_notification_referee


logger = logging.getLogger(__name__)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start bot")
    ])


def register_handlers(dp: Dispatcher):
    reg_handlers(dp)
    reg_registration(dp)
    reg_participant_notifications(dp)
    reg_participant_first_nomination(dp)
    reg_participant_second_notifications(dp)
    reg_participant_second_nomination(dp)
    reg_participant_third_notifications(dp)
    reg_participant_third_nomination(dp)
    reg_nomination_referee(dp)
    reg_participant_distib(dp)
    reg_notification_referee(dp)
