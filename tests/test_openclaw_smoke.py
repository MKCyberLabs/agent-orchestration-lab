"""Zero-token end-to-end smoke: REAL subprocesses, fake Codex binary, isolated Git."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

FAKE_CODEX = r'''#!/usr/bin/env python3
import json
from pathlib import Path
import sys
prompt = sys.stdin.read()
if 'TASK: TEST_ADD' in prompt:
    Path('math_ops.py').write_text('def add(a: int, b: int) -> int:\n    return a + b\n')
elif 'TASK: TEST_LABEL' in prompt:
    Path('text_ops.py').write_text('def normalize_label(value: str) -> str:\n    return " ".join(value.split())\n')
else:
    raise SystemExit('Unknown fixture task; refuse')
print(json.dumps({'type': 'turn.started'}))
print(json.dumps({'type': 'turn.completed', 'usage': {'total_tokens': 7}}))
'''


class RealSubprocessSmoke(unittest.TestCase):
    def test_two_tasks_in_real_shell_with_stub_cli(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            bindir = root / "bin"
            bindir.mkdir()
            codex = bindir / "codex"
            codex.write_text(FAKE_CODEX)
            codex.chmod(0o700)
            env = dict(os.environ)
            env["PATH"] = str(bindir) + os.pathsep + env.get("PATH", "")
            env["XDG_STATE_HOME"] = str(root / "state")
            env["HOME"] = str(root)
            p = subprocess.run(
                ["bash", str(ROOT / "scripts" / "openclaw-v04-smoke.sh"), "codex"],
                capture_output=True, text=True, cwd=root, env=env, timeout=90,
            )
            self.assertEqual(p.returncode, 0, p.stdout[-6500:] + "\nSTDERR:\n" + p.stderr[-4000:])
            self.assertIn("TEST_ADD | VERIFIED_COMMITTED", p.stdout)
            self.assertIn("TEST_LABEL | VERIFIED_COMMITTED", p.stdout)
            self.assertIn("Smoke command completed.", p.stdout)
            fixtures = list((root / "state" / "mk-nightshift-smoke").glob("fixture.*"))
            self.assertEqual(len(fixtures), 1)
            state = fixtures[0] / "state" / "fixture" / "state.json"
            self.assertTrue(state.exists())
            import json
            result = json.loads(state.read_text())
            self.assertEqual(result["window_completed"], 2)
            self.assertEqual(result["phase"], "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
