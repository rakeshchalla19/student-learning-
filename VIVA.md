# Viva preparation

1. **What problem does your project solve?** It organizes academic tasks and
   makes pending, completed and overdue work easy to review.
2. **Why Python?** It has readable syntax and standard-library support for the
   GUI, SQLite, CSV files and automated tests.
3. **What is Tkinter?** Python's interface to the Tk GUI toolkit. It provides
   windows, fields, buttons, dialogs and an event loop.
4. **What is SQLite?** A database engine that stores an entire database in a
   local file without a separate database server.
5. **What does CRUD mean?** Create, Read, Update and Delete. These correspond
   to INSERT, SELECT, UPDATE and DELETE SQL operations.
6. **Why separate app.py and database.py?** Presentation and storage have
   different responsibilities. The database rules can be tested without a GUI.
7. **What is a primary key?** A unique identifier for each row. Here it is the
   integer task ID; two tasks may have the same title but different IDs.
8. **How do you prevent SQL injection?** Pass values through SQL placeholders
   rather than inserting user text directly into query strings.
9. **How are invalid dates handled?** Python parses the calendar date and
   checks that the original text matches the YYYY-MM-DD representation.
10. **How does persistence work?** Writes are committed to a local database.
    Reopening the app reads the same file.
11. **What is a transaction?** A group of database operations committed together
    or rolled back if an error occurs.
12. **How is overdue calculated?** The due date is before today's local date
    and the task status is not Completed.
13. **How is completion calculated?** Completed task count divided by total
    task count, multiplied by 100. An empty task list reports zero.
14. **What is event-driven programming?** User actions trigger callbacks, such
    as saving a task when a button is clicked.
15. **Does it use AI or machine learning?** No. It uses deterministic validation,
    SQL operations and date comparisons.
16. **What are its limitations?** It is local and single-user, with no automatic
    notifications, mobile interface, account login or cloud synchronization.
17. **How would you extend it?** Add recurring-task rules, reminders and a
    calendar; a multi-user version would need authentication and a backend.
18. **What tests did you include?** Persistence and CRUD, literal search and
    filtering, invalid input, overdue rules, ordering and nonexistent updates.

## A short opening explanation

“My mini project is StudyTrack, a student study planner built with Python,
Tkinter and SQLite. Students can add academic tasks, assign deadlines and
priorities, and track completion. The dashboard shows progress and overdue work.
Data stays available after closing the app. I separated interface code from
database logic so that the business rules can be tested independently.”

Practice adding a field or changing a validation rule yourself so you can
explain the implementation, not just demonstrate the interface.
