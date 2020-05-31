import os
import telegram

bot_token = os.getenv('INPUT_BOTTOKEN')
# bot_token = '1122724836:AAF6K1XjbGfVykqoqUTARQA0Qa7A2ItEnZ8'
group_id = -1001328230896

def send(msg, chat_id=group_id, token=bot_token):
	bot = telegram.Bot(token=token)
	bot.sendMessage(chat_id=chat_id, text=msg)
