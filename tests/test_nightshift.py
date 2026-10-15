import importlib.util
import json
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

MODULE = Path(__file__).resolve().parents[1] / 'scripts' / 'nightshift.py'
spec = importlib.util.spec_from_file_location('nightshift', MODULE)
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


class NightshiftTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.task = self.root / 'task.md'
        self.task.write_text('Implement only a safe fixture change and run tests.')
        self.quota = self.root / 'quota.json'
        self.c = {'schema_version': 1, 'project_id': 'lab', 'worktree': str(self.root),
                  'task_file': str(self.task), 'quota_file': str(self.quota),
                  'state_dir': str(self.root/'state'), 'approved': True, 'agent': 'gemini',
                  'timezone': 'Asia/Kolkata', 'start': '00:15', 'stop': '05:15',
                  'quota_max_age_minutes': 30, 'min_quota_percent': 20}
        self.path = self.root / 'state.json'
        self.clock = datetime(2026, 10, 16, 1, 30, tzinfo=ZoneInfo('Asia/Kolkata'))
        self.quota.write_text(json.dumps({'checked_at': self.clock.isoformat(), 'agents': {'gemini': {'authenticated': True, 'remaining_percent': 75}}}))

    def test_window_in_and_out(self):
        self.assertEqual(n.active_window(self.c, self.clock), '2026-10-16')
        self.assertIsNone(n.active_window(self.c, self.clock.replace(hour=5, minute=15)))
        self.assertIsNone(n.active_window(self.c, self.clock.replace(hour=0, minute=14)))

    def test_window_cross_midnight(self):
        self.c['start'], self.c['stop'] = '23:00', '02:00'
        self.assertEqual(n.active_window(self.c, self.clock), '2026-10-15')
        self.assertIsNone(n.active_window(self.c, self.clock.replace(hour=3)))

    def test_quota_unknown_stale_and_low_fail_closed(self):
        self.assertEqual(n.quota_check(self.c, instant=self.clock), 75)
        with self.assertRaises(n.Hold):
            n.quota_check(self.c, instant=self.clock + timedelta(hours=1))
        self.c['min_quota_percent'] = 90
        with self.assertRaises(n.Hold):
            n.quota_check(self.c, instant=self.clock)
        self.c['min_quota_percent'] = 20
        self.quota.write_text(json.dumps({'checked_at': self.clock.isoformat(), 'agents': {'gemini': {'authenticated': True}}}))
        with self.assertRaises(n.Hold):
            n.quota_check(self.c, instant=self.clock)

    def test_write_atomic_private(self):
        n.atomic_write(self.path, {'phase': 'WAITING'})
        self.assertEqual(json.loads(self.path.read_text()), {'phase': 'WAITING'})
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_dispatch_once_and_resume_without_second_dispatch(self):
        calls = []
        def fake_cbds(_c, *args, **kwargs):
            calls.append(args[:2])
            if args[:2] == ('run', 'create'): return {'run_id': 'run_123'}
            if args[:2] == ('task', 'create'): return {'task_id': 'tsk_456'}
            if args[:2] == ('dispatch', 'start'): return {'dispatch_id': 'dsp_789'}
            if args[:2] == ('report', 'list'): return {'reports': []}
            raise AssertionError(args)
        with patch.object(n, 'ensure_preflight'), patch.object(n, 'cbds', side_effect=fake_cbds):
            initial = n.main_run(self.c, self.path, self.clock)
            second = n.main_run(self.c, self.path, self.clock)
        self.assertEqual(initial['phase'], 'WAITING')
        self.assertEqual(second['phase'], 'WAITING')
        self.assertEqual(calls.count(('dispatch', 'start')), 1)

    def test_crash_before_receipt_never_redispatches(self):
        for phase in n.AMBIGUOUS:
            with self.subTest(phase=phase):
                n.atomic_write(self.path, {'phase': phase, 'run_id': 'run_1'})
                with patch.object(n, 'cbds', side_effect=AssertionError('should not call cbds')):
                    state = n.main_run(self.c, self.path, self.clock)
                self.assertEqual(state['phase'], 'NEEDS_RECONCILIATION')

    def test_report_must_be_accepted(self):
        n.atomic_write(self.path, {'phase': 'WAITING', 'run_id': 'run_1', 'task_id': 'tsk_2'})
        with patch.object(n, 'cbds', return_value={'reports': [{'task_id': 'tsk_2', 'outcome': 'succeeded', 'accepted': False}]}):
            self.assertEqual(n.main_run(self.c, self.path, self.clock)['phase'], 'WAITING')
        with patch.object(n, 'cbds', return_value={'reports': [{'task_id': 'tsk_2', 'outcome': 'succeeded', 'accepted': True, 'report_id': 'rpt_3'}]}):
            result = n.main_run(self.c, self.path, self.clock)
        self.assertEqual(result['phase'], 'REVIEW_REQUIRED')
        self.assertEqual(result['report_id'], 'rpt_3')

    def test_unknown_report_schema_fails_closed(self):
        n.atomic_write(self.path, {'phase': 'WAITING', 'run_id': 'run_1', 'task_id': 'tsk_2'})
        with patch.object(n, 'cbds', return_value={'something': []}):
            self.assertEqual(n.main_run(self.c, self.path, self.clock)['phase'], 'NEEDS_RECONCILIATION')

    def test_refuse_unapproved_or_outside_window(self):
        self.c['approved'] = False
        with self.assertRaises(n.Hold), patch.object(n, 'cbds', side_effect=AssertionError):
            n.main_run(self.c, self.path, self.clock)
        self.c['approved'] = True
        with self.assertRaises(n.Hold), patch.object(n, 'cbds', side_effect=AssertionError):
            n.main_run(self.c, self.path, self.clock.replace(hour=15))

    def test_bad_identifiers_rejected(self):
        with self.assertRaises(n.Hold):
            n.id_from({'run_id': 'garbage'}, 'run')
        with self.assertRaises(n.Hold):
            n.id_from({'task_id': 'run_wrong'}, 'tsk')

    def test_config_is_strict(self):
        config = self.root/'config.json'
        config.write_text(json.dumps(self.c))
        self.assertEqual(n.load_config(config)['project_id'], 'lab')
        self.c['worktree'] = '../relative'
        config.write_text(json.dumps(self.c))
        with self.assertRaises(n.Hold):
            n.load_config(config)


if __name__ == '__main__':
    unittest.main()
