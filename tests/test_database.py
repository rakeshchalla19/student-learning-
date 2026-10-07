import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from database import TaskStore


class TaskStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'test.db'
        self.store = TaskStore(self.path)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def add(self, **changes):
        values = dict(title='Revise Java', subject='Programming', due=date.today().isoformat(),
                      priority='High', status='Pending', notes='Review classes')
        values.update(changes)
        return self.store.save(**values)

    def test_create_update_delete_and_restart(self):
        key = self.add()
        self.store.close()
        self.store = TaskStore(self.path)
        self.assertEqual(self.store.list()[0]['title'], 'Revise Java')
        self.add(task_id=key, status='Completed')
        self.assertEqual(self.store.summary(), (1, 1, 0))
        self.store.delete(key)
        self.assertEqual(self.store.list(), [])

    def test_search_and_filter(self):
        self.add(title="O'Reilly 100% SQL", notes='SQLite review')
        self.add(title='Physics', status='Completed')
        self.assertEqual(len(self.store.list('sqlite', 'Pending')), 1)
        self.assertEqual(len(self.store.list('%')), 1)
        self.assertEqual(self.store.list("' OR 1=1 --"), [])
        self.assertEqual(len(self.store.list(status='Completed')), 1)

    def test_invalid_input_leaves_database_unchanged(self):
        for values in ({'title': '  '}, {'subject': ''}, {'due': '2026-02-30'},
                       {'due': '20261007'}, {'priority': 'Urgent'}, {'status': 'Unknown'},
                       {'title': 'x' * 151}):
            with self.subTest(values=values), self.assertRaises(ValueError):
                self.add(**values)
        self.assertEqual(self.store.list(), [])

    def test_overdue_excludes_completed_and_today(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        self.add(due=yesterday)
        self.add(due=yesterday, status='Completed')
        self.add()
        self.assertEqual(self.store.summary(), (3, 1, 1))

    def test_order_by_completion_date_and_priority(self):
        self.add(title='Low', priority='Low')
        self.add(title='Done', status='Completed', due='2000-01-01')
        self.add(title='High')
        self.assertEqual([r['title'] for r in self.store.list()], ['High', 'Low', 'Done'])

    def test_missing_task_update_is_rejected(self):
        with self.assertRaises(ValueError):
            self.add(task_id=999)


if __name__ == '__main__':
    unittest.main()
