from pathlib import Path

import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(*args, code=0):
    script = next(ROOT.glob("*.py"))
    result = subprocess.run(
        [sys.executable, "-B", str(script), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"),
    )
    assert result.returncode == code, result.stderr
    return result.stdout


with tempfile.TemporaryDirectory() as temp:
    base = Path(temp)
    a, b = base / "a.csv", base / "b.csv"
    a.write_text("id,value\n1,a\n2,b\n")
    b.write_text("id,value\n1,c\n3,d\n")
    report = json.loads(run(a, b, "id"))
    assert report["added"][0]["id"] == "3" and report["removed"][0]["id"] == "2"
    assert report["changed"] == [dict(key="1", column="value", before="a", after="c")]
