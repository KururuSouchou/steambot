# _*_ coding:utf-8 _*_
from telegram.ext import CommandHandler
from .utils import get_price, set_user, get_user


start_text = u"""Just tell me your *Steam Community* ID.
告訴我你的*Steam社區*ID。
"""


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text=start_text,
        parse_mode="Markdown",
    )


def price(bot, update):
    user_id = "user_%s" % update.message.from_user.id
    games = db_get_list(user_id)
    for i in games:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=i + "\r\n" + get_price(
                i, get_user(update.message.from_user.id)
                ),
            parse_mode="Markdown",
            reply_to_message_id=update.message.message_id
        )


start_command_handler = CommandHandler('start', start)
price_command_handler = CommandHandler('price', price)

