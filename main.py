import os
import sys
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from schedule_session import schedule_subject, list_schedules, stop_schedule

sys.dont_write_bytecode = True

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN", "")

if not TOKEN:
    print("Please set the TOKEN.")

if __name__ == "__main__":
    print("Starting Bot...")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("schedule", schedule_subject))
    application.add_handler(CommandHandler("list", list_schedules))
    application.add_handler(CommandHandler("stop", stop_schedule))

    print("Polling...")
    application.run_polling()
