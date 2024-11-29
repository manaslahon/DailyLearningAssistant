from datetime import datetime
from telegram import CallbackGame, Update
from telegram.ext import CallbackContext
from database import ProgressTrackerDB

progress = {}


async def start_study(update: Update, context: CallbackContext):
    try:
        subject = context.args[0]
        start_time = datetime.now().isoformat()
        start_date = datetime.today().date()
        chat_id = update.message.chat.id

        with ProgressTrackerDB() as db:
            db.save_progress(subject, chat_id, start_time, None, None, start_date)
        await update.message.reply_text(f"Session started for the subject {subject}")

    except IndexError:
        await update.message.reply_text("Usage: /start <subject>. Example: /start math")


async def finish_study(update: Update, context: CallbackContext):
    try:
        subject = context.args[0]
        end_time = datetime.now()
        chat_id = update.message.chat.id

        with ProgressTrackerDB() as db:
            results = db.load_progress(subject)
            progress[subject] = [
                {
                    "start_time": row[0],
                    "end_time": row[1],
                    "duration": row[2],
                    "start_date": row[3],
                    "chat_id": row[4],
                }
                for row in results
                if row[4] == chat_id
            ]
        for session in progress[subject]:
            if session["end_time"] is None:
                start_time_dt = datetime.fromisoformat(session["start_time"])
                duration = (end_time - start_time_dt).total_seconds() / 3600

                with ProgressTrackerDB() as db:
                    db.update_progress(
                        subject,
                        session["start_time"],
                        end_time.isoformat(),
                        duration,
                        session["start_date"],
                        chat_id,
                    )

        await update.message.reply_text(f"Session for {subject} has ended.")

    except IndexError:
        await update.message.reply_text(
            "Usage: /finish <subject>. Example: /finish math"
        )

    except Exception as e:
        await update.message.reply_text(f"Failed to end the session: {e}")


async def show_progress(update: Update, context: CallbackContext):
    try:
        subject = context.args[0]
        chat_id = update.message.chat.id

        with ProgressTrackerDB() as db:
            results = db.load_progress(subject)
            progress[subject] = [
                {
                    "start_time": row[0],
                    "end_time": row[1],
                    "duration": row[2],
                    "start_date": row[3],
                    "chat_id": row[4],
                }
                for row in results
                if row[4] == chat_id
            ]

        if not progress[subject]:
            await update.message.reply_text(f"No progress data found for {subject}.")
            return

        message = f"Progress for {subject}:\n"
        for session in progress[subject]:
            start_time_dt = datetime.fromisoformat(session["start_time"])
            end_time = session["end_time"]
            duration = session["duration"]
            formatted_duration = f"{duration:.2f} hours" if duration else "In progress"
            message += (
                f"Started: {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Ended: {end_time if end_time else 'Ongoing'}\n"
                f"Duration: {formatted_duration}\n\n"
            )

        await update.message.reply_text(message)

    except IndexError:
        await update.message.reply_text(
            "Usage: /progress <subject>. Example: /progress math"
        )

    except Exception as e:
        await update.message.reply_text(f"Failed to show progress: {e}")
