from aiogram import Dispatcher
import logging

from aiogram import types

from handlers.commands import register as reg_handlers
from handlers.registration import register as reg_registration
from handlers.participant.first_notifications import register as reg_participant_notifications
from handlers.participant.first_nomination import register as reg_first_nomination

logger = logging.getLogger(__name__)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start bot")
    ])


def register_handlers(dp: Dispatcher):
    reg_handlers(dp)
    reg_registration(dp)
    reg_participant_notifications(dp)
    reg_first_nomination(dp)
