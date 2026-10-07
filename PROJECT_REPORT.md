# StudyTrack: Student Study Planner

**Student:** Rakesh Challa  
**Project type:** Desktop application mini project  
**Technology:** Python, Tkinter, SQLite  
**Institution / roll number / guide:** Fill in before submission

## Abstract

Students often track academic tasks across notebooks and messages, making it
difficult to see approaching deadlines and unfinished work. StudyTrack provides
a single desktop interface to record tasks, set priorities, track completion and
review overdue work. SQLite stores the records locally and Tkinter provides the
graphical interface. The application works offline and exports filtered records
to CSV. It is a small, understandable demonstration of CRUD operations, input
validation, event-driven programming and persistent storage.

## Problem statement and objectives

Build a local application that organizes academic tasks and makes their status
visible. Objectives are to support reliable creation and editing, prevent invalid
records, identify missed deadlines, calculate completion progress, and retain
records after the application closes.

## Existing approach and proposed solution

Paper lists require manual counting and searching. Unstructured notes may omit
dates or status. The proposed solution stores consistent task fields and offers
search, filtering and a dashboard. It is intended for personal planning, and
does not claim to improve grades or provide predictive analytics.

## Requirements

- Python 3.10+, Tkinter, SQLite support and a graphical desktop session.
- A writable home directory for local data.
- Windows, macOS or Linux with the required Python components.
- No external database server or third-party Python package is required.

## Architecture

The presentation layer (`app.py`) receives form input and handles user events.
It calls the storage layer (`database.py`), which validates data and executes
parameterized SQL statements. SQLite persists data in `tasks.db`. Returned rows
populate the task table and dashboard. CSV export uses the visible result set.

## Database design

| Field | SQLite type | Purpose |
|---|---|---|
| id | INTEGER PRIMARY KEY | Unique task identifier |
| title | TEXT NOT NULL | Task name, maximum 150 characters |
| subject | TEXT NOT NULL | Academic subject, maximum 80 characters |
| due | TEXT NOT NULL | Valid date in YYYY-MM-DD format |
| priority | TEXT NOT NULL | High, Medium or Low |
| status | TEXT NOT NULL | Pending, In progress or Completed |
| notes | TEXT NOT NULL | Optional notes, maximum 5000 characters |

Allowed values and lengths are validated in Python. The SQLite schema enforces
primary-key uniqueness and non-null fields; it does not independently enforce
every business rule if edited outside the app.

## Main algorithms

1. Validate nonblank task title and subject, field lengths, calendar date and
   allowed priority/status values.
2. Insert a new record or update the selected record in a transaction.
3. Query records with unfinished tasks first, due dates ascending and higher
   priority first for the same date.
4. Apply case-insensitive literal search and the selected status filter.
5. Calculate `completion percentage = completed / total × 100`, using zero
   when no tasks exist.
6. Count unfinished tasks with a due date earlier than today's local date.

Searching is O(n) over the returned records. The database sort can require
O(n log n) work without a matching index. This is appropriate for a small
personal task list; larger deployments would need database-side search,
pagination and indexing.

## Reliability and data handling

SQL parameters keep text separate from query syntax. Transactions make each
write atomic. Delete requires confirmation. CSV text beginning with formula-like
characters is prefixed with an apostrophe. The application stores data locally
without encryption and assumes a trusted single-user desktop account.

## Testing

The included unittest suite exercises saved data after reopening, CRUD operations,
literal search, filtering, invalid dates, blank fields, allowed values, overdue
counts, sort order and missing-record updates. A manual demonstration should
check form interaction, selection, dialog cancellation, CSV output and layout.
Automated database tests do not establish that every desktop platform has been
visually tested.

## Future scope

Recurring tasks, optional reminders, backup/restore controls, calendar view,
multi-device synchronization and authenticated accounts could extend the app.
These are proposed extensions and are not included in this implementation.

## Conclusion

StudyTrack demonstrates a complete local task-management workflow through a
small layered application. The project provides practical examples of Python
classes, GUI events, SQL, validation, persistence and automated testing.
