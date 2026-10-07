"""Validated task storage. Uses only the Python standard library."""
import sqlite3
from datetime import date
from pathlib import Path

PRIORITIES = ('High', 'Medium', 'Low')
STATUSES = ('Pending', 'In progress', 'Completed')


class TaskStore:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, title TEXT NOT NULL, subject TEXT NOT NULL,
            due TEXT NOT NULL, priority TEXT NOT NULL, status TEXT NOT NULL,
            notes TEXT NOT NULL)''')
        self.connection.commit()

    def save(self, title, subject, due, priority, status, notes='', task_id=None):
        title, subject, notes = title.strip(), subject.strip(), notes.strip()
        if not title or not subject:
            raise ValueError('Enter a task title and subject.')
        if len(title) > 150 or len(subject) > 80 or len(notes) > 5000:
            raise ValueError('Maximum lengths: title 150, subject 80, notes 5000.')
        try:
            parsed = date.fromisoformat(due)
            if parsed.isoformat() != due:
                raise ValueError()
        except (ValueError, TypeError):
            raise ValueError('Enter a valid due date as YYYY-MM-DD.') from None
        if priority not in PRIORITIES or status not in STATUSES:
            raise ValueError('Choose a valid priority and status.')
        values = (title, subject, due, priority, status, notes)
        with self.connection:
            if task_id is None:
                cursor = self.connection.execute(
                    'INSERT INTO tasks (title, subject, due, priority, status, notes) VALUES (?,?,?,?,?,?)', values)
                return cursor.lastrowid
            cursor = self.connection.execute(
                'UPDATE tasks SET title=?, subject=?, due=?, priority=?, status=?, notes=? WHERE id=?',
                (*values, task_id))
            if cursor.rowcount != 1:
                raise ValueError('Task no longer exists. Refresh the list.')
            return task_id

    def list(self, query='', status='All'):
        # Search in Python so %, _ and quotes are treated as literal text.
        rows = self.connection.execute('''SELECT * FROM tasks ORDER BY
            CASE WHEN status='Completed' THEN 1 ELSE 0 END, due,
            CASE priority WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, id''').fetchall()
        needle = query.casefold().strip()
        return [dict(row) for row in rows
                if (status == 'All' or row['status'] == status)
                and needle in (row['title'] + ' ' + row['subject'] + ' ' + row['notes']).casefold()]

    def delete(self, task_id):
        with self.connection:
            self.connection.execute('DELETE FROM tasks WHERE id=?', (task_id,))

    def summary(self):
        tasks = self.list()
        done = sum(t['status'] == 'Completed' for t in tasks)
        overdue = sum(t['status'] != 'Completed' and t['due'] < date.today().isoformat() for t in tasks)
        return len(tasks), done, overdue

    def close(self):
        self.connection.close()


def default_database():
    folder = Path.home() / '.studytrack'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / 'tasks.db'
