from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext



async def start_study(update:Update, context: CallbackContext):
    try:
        subject = context.args[0]
        start_time = datetime.now().isoformat()
        chat_id = update.message.chat.id
        

