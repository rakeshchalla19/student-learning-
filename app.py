"""StudyTrack desktop entry point: python app.py"""
import csv
import sqlite3
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox, filedialog
from database import TaskStore, default_database, PRIORITIES, STATUSES


class StudyTrack:
    def __init__(self, root, store):
        self.root, self.store, self.selected = root, store, None
        root.title('StudyTrack | Student Study Planner')
        root.geometry('1120x720')
        root.minsize(900, 650)
        root.configure(bg='#f0f4f8')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f4f8')
        style.configure('TLabel', background='#f0f4f8', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10), padding=8)
        style.configure('Treeview', rowheight=32, font=('Segoe UI', 10))
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        header = tk.Frame(root, bg='#142d4e', padx=24, pady=18)
        header.pack(fill='x')
        tk.Label(header, text='StudyTrack', bg='#142d4e', fg='white',
                 font=('Segoe UI', 25, 'bold')).pack(anchor='w')
        tk.Label(header, text='Plan your work. Track your progress.', bg='#142d4e',
                 fg='#a9d9e8', font=('Segoe UI', 11)).pack(anchor='w')
        main = ttk.Frame(root, padding=20)
        main.pack(fill='both', expand=True)
        self.stats = ttk.Label(main, font=('Segoe UI', 13, 'bold'))
        self.stats.pack(anchor='w', pady=(0, 8))
        self.progress = ttk.Progressbar(main, maximum=100)
        self.progress.pack(fill='x', pady=(0, 18))
        body = ttk.Frame(main)
        body.pack(fill='both', expand=True)
        form = ttk.Frame(body, padding=(0, 0, 20, 0))
        form.pack(side='left', fill='y')
        self.form_title = ttk.Label(form, text='New task', font=('Segoe UI', 15, 'bold'))
        self.form_title.pack(anchor='w', pady=(0, 10))
        self.fields = {}
        for key, label, choices in [('title', 'Task title', None), ('subject', 'Subject', None),
                                   ('due', 'Due date · YYYY-MM-DD', None),
                                   ('priority', 'Priority', PRIORITIES), ('status', 'Status', STATUSES)]:
            ttk.Label(form, text=label).pack(anchor='w', pady=(7, 3))
            variable = tk.StringVar()
            self.fields[key] = variable
            widget = (ttk.Combobox(form, textvariable=variable, values=choices, state='readonly', width=27)
                      if choices else ttk.Entry(form, textvariable=variable, width=30))
            widget.pack(fill='x')
        ttk.Label(form, text='Notes').pack(anchor='w', pady=(10, 3))
        self.notes = tk.Text(form, width=28, height=5, wrap='word', font=('Segoe UI', 10))
        self.notes.pack(fill='x')
        ttk.Button(form, text='Save task', command=self.save).pack(fill='x', pady=(12, 4))
        ttk.Button(form, text='New / clear form', command=self.clear).pack(fill='x')
        panel = ttk.Frame(body)
        panel.pack(side='left', fill='both', expand=True)
        controls = ttk.Frame(panel)
        controls.pack(fill='x', pady=(0, 10))
        ttk.Label(controls, text='Search').pack(side='left')
        self.search = tk.StringVar()
        ttk.Entry(controls, textvariable=self.search, width=20).pack(side='left', fill='x', expand=True, padx=8)
        self.filter = tk.StringVar(value='All')
        ttk.Combobox(controls, values=('All', *STATUSES), textvariable=self.filter,
                     state='readonly', width=14).pack(side='left')
        grid = ttk.Frame(panel)
        grid.pack(fill='both', expand=True)
        columns = ('title', 'subject', 'due', 'priority', 'status')
        self.tree = ttk.Treeview(grid, columns=columns, show='headings', selectmode='browse')
        for key, width in zip(columns, (190, 110, 105, 75, 110)):
            self.tree.heading(key, text=key.title())
            self.tree.column(key, width=width, minwidth=60)
        self.tree.tag_configure('overdue', foreground='#b42318')
        self.tree.tag_configure('done', foreground='#18734b')
        scroll = ttk.Scrollbar(grid, orient='vertical', command=self.tree.yview)
        horizontal = ttk.Scrollbar(grid, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll.set, xscrollcommand=horizontal.set)
        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')
        horizontal.grid(row=1, column=0, sticky='ew')
        grid.rowconfigure(0, weight=1)
        grid.columnconfigure(0, weight=1)
        actions = ttk.Frame(panel)
        actions.pack(fill='x', pady=10)
        ttk.Button(actions, text='Edit selected', command=self.edit).pack(side='left')
        ttk.Button(actions, text='Delete selected', command=self.delete).pack(side='left', padx=8)
        ttk.Button(actions, text='Export CSV', command=self.export).pack(side='right')
        self.feedback = ttk.Label(panel, text='Select a task and click Edit to update it. Red rows indicate overdue tasks.', wraplength=580)
        self.feedback.pack(anchor='w')
        self.tree.bind('<Double-1>', lambda event: self.edit())
        self.search.trace_add('write', lambda *args: self.refresh())
        self.filter.trace_add('write', lambda *args: self.refresh())
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.clear()
        self.refresh()

    def clear(self):
        self.selected = None
        for key, value in {'title': '', 'subject': '', 'due': date.today().isoformat(),
                           'priority': 'Medium', 'status': 'Pending'}.items():
            self.fields[key].set(value)
        self.notes.delete('1.0', 'end')
        self.form_title.configure(text='New task')

    def refresh(self):
        self.rows = self.store.list(self.search.get(), self.filter.get())
        self.tree.delete(*self.tree.get_children())
        for row in self.rows:
            tag = 'done' if row['status'] == 'Completed' else ('overdue' if row['due'] < date.today().isoformat() else '')
            self.tree.insert('', 'end', iid=str(row['id']), values=[row[k] for k in ('title', 'subject', 'due', 'priority', 'status')], tags=(tag,))
        total, done, overdue = self.store.summary()
        self.stats.configure(text=f'{total} total tasks     •     {done} completed     •     {overdue} overdue')
        self.progress['value'] = 100 * done / total if total else 0

    def save(self):
        try:
            self.store.save(**{key: value.get() for key, value in self.fields.items()},
                            notes=self.notes.get('1.0', 'end-1c'), task_id=self.selected)
        except (ValueError, sqlite3.Error) as error:
            messagebox.showerror('Could not save', str(error))
            return
        self.clear()
        self.refresh()
        self.feedback.configure(text='Task saved. Search and status filters still apply.')

    def chosen(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo('Select a task', 'Select a task in the list first.')
            return None
        return next((r for r in self.rows if r['id'] == int(selection[0])), None)

    def edit(self):
        row = self.chosen()
        if row is None:
            return
        self.selected = row['id']
        for key, variable in self.fields.items():
            variable.set(row[key])
        self.notes.delete('1.0', 'end')
        self.notes.insert('1.0', row['notes'])
        self.form_title.configure(text='Edit task')

    def delete(self):
        row = self.chosen()
        if row and messagebox.askyesno('Delete task?', f'Delete "{row["title"]}"? This cannot be undone.'):
            try:
                self.store.delete(row['id'])
            except sqlite3.Error as error:
                messagebox.showerror('Could not delete', str(error))
                return
            if self.selected == row['id']:
                self.clear()
            self.refresh()

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='studytrack-tasks.csv', filetypes=[('CSV files', '*.csv')])
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8-sig') as stream:
                writer = csv.DictWriter(stream, fieldnames=('id', 'title', 'subject', 'due', 'priority', 'status', 'notes'))
                writer.writeheader()
                for row in self.rows:
                    # Prevent user-entered text from becoming spreadsheet formulas.
                    writer.writerow({k: "'" + v if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@')) else v for k, v in row.items()})
        except OSError as error:
            messagebox.showerror('Export failed', str(error))
            return
        self.feedback.configure(text=f'Exported {len(self.rows)} visible tasks.')

    def close(self):
        self.store.close()
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    try:
        store = TaskStore(default_database())
    except (OSError, sqlite3.Error) as error:
        root.withdraw()
        messagebox.showerror('StudyTrack could not start', str(error))
        root.destroy()
    else:
        StudyTrack(root, store)
        root.mainloop()
