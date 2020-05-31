import os
import telegram

bot_token = os.getenv('INPUT_BOTTOKEN')
group_id = int(os.getenv('INPUT_GROUPID') or 0)

def send(msg, chat_id=group_id, token=bot_token):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
