
import sqlite3
from pathlib import Path

# Store the database in the project root directory.
DB_PATH = Path(__file__).resolve().parent.parent / "openflow.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)


def get_all_tasks():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }
        for row in rows
    ]


def add_task(title: str):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,),
        )
        task_id = cursor.lastrowid

        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"]),
    }


def toggle_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        new_done = 0 if row["done"] else 1

        connection.execute(
            "UPDATE tasks SET done = ? WHERE id = ?",
            (new_done, task_id),
        )

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(new_done),
        }


def remove_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            return None

        task = {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }

        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )

        return task


init_db()
