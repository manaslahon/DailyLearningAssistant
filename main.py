import os
import sys
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from schedule_session import schedule_subject, list_schedules, stop_schedule
from progress_tracker import finish_study, show_progress, start_study

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
    application.add_handler(CommandHandler("start", start_study))
    application.add_handler(CommandHandler("finish", finish_study))
    application.add_handler(CommandHandler("progress", show_progress))

    print("Polling...")
    application.run_polling()
