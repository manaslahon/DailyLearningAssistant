# Daily Learning Assistant Bot

The Daily Learning Assistant Bot is a personal study assistant designed to help you schedule learning sessions, track progress, and receive reminders. It is implemented as a Telegram bot and integrates a database for tracking study sessions and generating progress reports.
## Features

    Study Scheduling: Schedule study sessions for different subjects.
    Progress Tracking: Automatically record start and end times of study sessions, and calculate the duration spent on each subject.
    Reminders: Set reminders for study sessions to keep you on track.
    Progress Reports: View a summary of your study habits, including time spent on each subject over time.

## Technologies Used

    Python: The main programming language.
    SQLite/MySQL: Database for storing study session data.
    APScheduler: For scheduling study reminders.
    Telegram Bot API: For handling bot communication.
    SQLAlchemy: Database ORM for managing database operations.

## Setup and Installation
### Prerequisites

    - Python 3.x
    - A Telegram account and bot token from BotFather.
    - SQLite or MySQL for the database.

### Installation Steps

#### 1. Clone the Repository:
```bash
git clone https://github.com/your-username/daily-learning-assistant-bot.git
cd daily-learning-assistant-bot
```
#### 2. Install the Dependencies:

Install the required Python packages by running:
```bash
pip install -r requirements.txt
```
#### 3. Set Up the Database:

    For SQLite: The database will automatically be created as `study_sessions.db`.
    For MySQL: Update the connection string in the `ProgressTrackerDB` class with your MySQL credentials.

#### 4. Configure the Bot Token:

    - Create a .env file in the root directory.

    - Add your Telegram bot token:

    - BOT_TOKEN=<your-telegram-bot-token>

#### 5. Run the Bot:

Start the bot by running the following command:
```bash
    python bot.py
```
Usage

    - Start a Study Session: Use the /start command to begin interacting with the bot.
    - Schedule a Study Session: Use the /schedule command to schedule study sessions for specific subjects.
    - View Progress: Use the /progress command to view how much time you’ve spent on each subject.
    - Cancel a Session: Use the /cancel command to remove a scheduled study session.

Example Commands

    - /schedule SubjectA 09:00-10:00: Schedules a study session for "SubjectA" from 9:00 AM to 10:00 AM.
    - /progress: Shows a summary of your study times by subject.

Database Structure

The bot uses a simple database schema to store study sessions. The key table is:

    study_sessions: Tracks all study sessions with the following columns:
        id: Unique session ID.
        subject: The subject being studied.
        chat_id: Telegram user ID.
        start_time: Start time of the session.
        end_time: End time of the session.
        duration: Duration of the study session.
        date: Date of the session.
