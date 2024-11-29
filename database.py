import os
import sqlite3


if not os.path.exists("data"):
    os.makedirs("data")


class SchedulesDB:

    def __init__(self, db_name="data/schedules.db") -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.c.execute(
            """ CREATE TABLE IF NOT EXISTS schedules
        (subject TEXT, chat_id INTEGER, run_time TEXT)"""
        )

    def save_schedule(self, subject, chat_id, run_time):
        self.c.execute(
            "INSERT INTO schedules (subject, chat_id, run_time) VALUES (?,?,?)",
            (subject, chat_id, run_time),
        )

    def delete_schedule(self, subject):
        self.c.execute("DELETE FROM schedules WHERE subject=?", (subject,))

    def load_schedules(self):
        self.c.execute("SELECT subject, chat_id, run_time FROM schedules")
        return self.c.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.conn.commit()
        else:
            print(
                f"There was an error while saving to the database: {exc_type}, {exc_value}"
            )
        self.conn.close()


class ProgressTrackerDB:

    def __init__(self, db_name="data/progress.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS study_sessions(
            subject TEXT, chat_id INTEGER, start_time TEXT, end_time TEXT, duration REAL, date DATE
                       )"""
        )

    def save_progress(self, subject, chat_id, start_time, end_time, duration, date):
        self.c.execute(
            """INSERT INTO study_sessions VALUES(?,?,?,?,?,?)""",
            (subject, chat_id, start_time, end_time, duration, date),
        )

    def load_progress(self, subject):
        self.c.execute(
            """SELECT start_time, end_time, duration, date, chat_id FROM study_sessions WHERE subject=?""",
            (subject,),
        )
        return self.c.fetchall()

    def update_progress(self, subject, start_time, end_time, duration, date, chat_id):
        self.c.execute(
            """UPDATE study_sessions SET end_time=?, duration=? WHERE subject=? AND start_time=? AND date=? AND chat_id=?""",
            (
                end_time,
                duration,
                subject,
                start_time,
                date,
                chat_id,
            ),
        )

    def delete_progress(self, subject):
        self.c.execute(
            """DELETE FROM study_sessions WHERE subject=?""",
            (subject,),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.conn.commit()
        else:
            print(
                f"There was an error while saving to the database: {exc_type}, {exc_value}"
            )
        self.conn.close()
