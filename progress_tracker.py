from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from database import ProgressTrackerDB

progress = {}


# Command to start a study session
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


# Command to finish a study session
async def finish_study(update: Update, context: CallbackContext):
    try:
        subject = context.args[0]
        end_time = datetime.now()
        chat_id = update.message.chat.id

        # Load progress from the database
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

        # Find ongoing sessions (where end_time is None) and update them
        for session in progress[subject]:
            if session["end_time"] is None:
                start_time_dt = datetime.fromisoformat(session["start_time"])
                duration = (end_time - start_time_dt).total_seconds() / 3600

                # Update the session in the database with the end time and duration
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


# Command to show the progress of study sessions
async def show_progress(update: Update, context: CallbackContext):
    try:
        subject = context.args[0]
        chat_id = update.message.chat.id

        # Load progress from the database
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

        # If no progress data found for the subject
        if not progress[subject]:
            await update.message.reply_text(f"No progress data found for {subject}.")
            return

        # Prepare the message showing the progress
        message = f"Progress for {subject}:\n"
        for session in progress[subject]:
            start_time_dt = datetime.fromisoformat(session["start_time"])

            # Handle the case where end_time is None (session is ongoing)
            if session["end_time"]:
                end_time_dt = datetime.fromisoformat(session["end_time"]).strftime(
                    "%H:%M:%S"
                )
            else:
                end_time_dt = "Ongoing"

            # Format the duration, showing "In progress" if duration is None
            duration = session["duration"]
            formatted_duration = f"{duration:.2f} hours" if duration else "In progress"

            # Build the message for each session
            message += (
                f"Started: {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"Ended: {end_time_dt}\n"
                f"Duration: {formatted_duration}\n\n"
            )

        # Send the progress message to the user
        await update.message.reply_text(message)

    except IndexError:
        await update.message.reply_text(
            "Usage: /progress <subject>. Example: /progress math"
        )

    except Exception as e:
        await update.message.reply_text(f"Failed to show progress: {e}")
