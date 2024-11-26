import pytz
from telegram import Update
from datetime import datetime
from database import SchedulesDB
from telegram.ext import CallbackContext
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

# dictionary to store scheduled jobs

scheduled_jobs = {}


async def schedule_subject(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /schedule <subject> <time>. Example: /schedule math 5pm"
        )
        return

    try:
        subject = context.args[0]
        time = context.args[1]

        time_obj = convert_time_to_24hr(time)

        if time_obj:
            formatted_time = time_obj.strftime("%I:%M %p")  # e.g., 05:00 PM
            chat_id = update.message.chat.id
            job = schedule_study_reminder(chat_id, subject, time_obj, context)
            scheduled_jobs[subject] = job  # storing the job at the key as subject

            with SchedulesDB() as db:
                db.save_schedule(subject, chat_id, time_obj.isoformat())

            await update.message.reply_text(
                f"Study session for {subject} scheduled at {formatted_time}"
            )
        else:
            await update.message.reply_text(
                'Invalid time format. Please use something like "5pm" or "17:00"'
            )
    except (IndexError, ValueError):
        await update.message.reply_text(
            "Usage: /schedule <subject> <time>. Example: /schedule math 5pm"
        )


def convert_time_to_24hr(time: str):
    try:
        time_obj = datetime.strptime(time, "%I%p")  # handles input such as 5pm
        tz = pytz.timezone("America/New_York")  # Sets preferred timezone
        time_obj = tz.localize(time_obj)
        return time_obj
    except ValueError:
        try:
            time_obj = datetime.strptime(time, "%H:%M")  # handles input such as 17:00
            tz = pytz.timezone("America/New_York")  # Sets preferred timezone
            time_obj = tz.localize(time_obj)
            return time_obj
        except ValueError:
            return None


def schedule_study_reminder(
    chat_id: int, subject: str, time_obj: datetime, context: CallbackContext
):
    job = scheduler.add_job(
        send_study_reminder, "date", run_date=time_obj, args=[chat_id, subject, context]
    )
    return job


def send_study_reminder(chat_id: int, subject: str, context: CallbackContext):
    context.bot.send_message(chat_id=chat_id, text=f"Time to study {subject}!")


async def list_schedules(update: Update, context: CallbackContext) -> None:
    with SchedulesDB() as db:
        schedules = db.load_schedules()
        for subject, chat_id, run_time in schedules:
            scheduled_time = datetime.fromisoformat(run_time)
            job = schedule_study_reminder(chat_id, subject, scheduled_time, context)
            scheduled_jobs[subject] = job

    if scheduled_jobs:
        message = "Here are your scheduled sessions:\n\n"
        index = 1
        for subject, job in scheduled_jobs.items():
            run_time = job.next_run_time.strftime("%I:%M %p")
            message += f"{index}) {subject} at {run_time}\n"
            index += 1
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("No scheduled study sessions found.")


async def stop_schedule(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /stop <subject>. Example: /stop math")
        return
    subject = context.args[0]
    try:
        job = scheduled_jobs.pop(subject, None)
        if job:
            scheduler.remove_job(job.id)
            with SchedulesDB() as db:
                db.delete_schedule(subject)
            await update.message.reply_text(
                f"Study session for {subject} has been cancelled."
            )
        else:
            await update.message.reply_text(
                f"No scheduled sessions found for {subject}."
            )
    except JobLookupError:
        await update.message.reply_text(
            f"Failed to cancel study session for the subject {subject}."
        )
