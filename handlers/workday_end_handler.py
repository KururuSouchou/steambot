from telegram.ext import BaseFilter, Filters, MessageHandler
from utils import set_user
from steam_api.users import User, UserDoesNotExistError
import json

crf = open('config.json')
config = json.load(crf)
api_key = config['api_key']
crf.close()


class WorkdayEndFilter(BaseFilter):

    def filter(self, message):
        return True


def set_user_id(bot, update):
    steam_user = update.message.text
    u = User(steam_user, api_key)
    try:
        username = u.check_account()
        set_user(update.message.from_user.id, steam_user)
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u"Weclome, {}".format(username),
            reply_to_message_id=update.message.message_id
        )
    except UserDoesNotExistError:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u"無法獲取用戶信息，請檢查用戶ID",
            reply_to_message_id=update.message.message_id
        )
    except:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u"網路連接錯誤，請稍後重試",
            reply_to_message_id=update.message.message_id
        )


dealhigh_handler = MessageHandler(
    Filters.text & WorkdayEndFilter(),
    set_user_id
)
