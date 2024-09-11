"""The (second) simplest grader.

This runs the student submission, and without checking the output
gives them a 100%. However, if the submission crashes the student will get a 0%
"""

from __future__ import annotations

import subprocess
import sys

process = subprocess.run([sys.executable, sys.argv[1]], check=False)
if process.returncode != 0:
    print("Encountered exception for test case 0:")
    print(process.stderr)
    print("Score: 0%")
else:
    print("Score: 100%")
