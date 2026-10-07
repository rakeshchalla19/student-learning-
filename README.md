# StudyTrack — Student Study Planner

A beginner-friendly Python mini project that helps students organize assignments,
study sessions and deadlines. Built with Tkinter and SQLite; no pip packages,
API keys or internet connection are required to use it.

Prepared for **Rakesh Challa** · GitHub: https://github.com/rakeshchalla19

## Features

- Create, edit and delete tasks with subjects, deadlines, priorities and notes.
- Track Pending, In progress and Completed work.
- Search titles, subjects and notes; filter by status.
- View overall completion progress and overdue counts.
- Sort unfinished tasks before completed tasks, then by due date and priority.
- Export the currently visible tasks to a spreadsheet-compatible CSV file.
- Save tasks automatically in a local SQLite database between sessions.

## Run on Windows

1. Install Python 3.10 or later with Tcl/Tk support. The standard Windows installer
   normally includes it. Select **Add Python to PATH** during installation.
2. Download or clone this repository and open the folder containing `app.py` in VS Code.
3. Open **Terminal → New Terminal**, then run:

```powershell
py app.py
```

If `py` is unavailable, try `python app.py`. No virtual environment or pip install
is required. To check Tkinter independently, run `python -m tkinter`.

On macOS/Linux, run `python3 app.py` in a graphical desktop session. Some Linux
Python installations require the distribution's Tkinter package (`python3-tk`
on Debian/Ubuntu). A phone, headless terminal or browser cannot run this desktop UI.

## Quick demonstration

1. Add “Complete Java assignment”, subject “Programming”, with a valid due date.
2. Add a second task with yesterday's date to demonstrate the overdue indicator.
3. Select the first task, click **Edit selected**, change its status to Completed,
   and save. Show the progress bar changing.
4. Search “Java”, then filter Completed. Clear the search and choose All afterward.
5. Export CSV; close and reopen the app to demonstrate persistence.

The dashboard always describes **all tasks**. Search and status filters affect the
table and CSV export. A due date becomes overdue on the following local calendar
day; completed tasks never count as overdue. Tasks are local to your computer.

## Project structure

```text
studytrack/
  app.py                  Desktop interface, events and CSV export
  database.py             Validation, queries and database persistence
  tests/test_database.py  Automated storage and business-rule tests
  PROJECT_REPORT.md       Academic explanation and demonstration plan
  VIVA.md                 Questions and answers for project discussion
  README.md               Setup and usage
  .gitignore              Excludes private data and generated files
  .github/workflows/tests.yml  GitHub Actions test workflow
```

## Test

From this folder:

```powershell
python -m unittest discover -s tests -v
```

Automated tests cover persistence, update/delete, search/filter, invalid input,
overdue rules, sort order and updates of nonexistent tasks. They use temporary
databases and do not modify your real tasks. GUI layout and interactions should
also be checked manually using the demonstration above.

## Data and backup

The database lives at `~/.studytrack/tasks.db` (on Windows, usually
`C:\Users\YOUR_NAME\.studytrack\tasks.db`). Close the app before copying this
file for a backup. CSV is an export, not a database backup or import format.
Do not commit personal task databases to GitHub.

## Repository

https://github.com/rakeshchalla19/student-learning-

Use **Code → Download ZIP** to download the source, or clone this repository.
Open the extracted folder containing `app.py` before running the commands above.

## Limitations and next steps

This is a single-user desktop mini project. It does not send notifications,
authenticate multiple users, synchronize devices, or import CSV. Possible
extensions: reminders, recurring tasks, charts and a web/mobile interface.

Review and understand the code before submission, adapt it to your college's
requirements, and follow any required disclosure rules for AI assistance.
