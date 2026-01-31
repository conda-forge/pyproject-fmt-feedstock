import sys
from subprocess import call
import site
from pathlib import Path
from typing import Any

try:
    __import__("abi3audit")
    IS_ABI3 = True
except ImportError:
    IS_ABI3 = False


WIN = sys.platform == "win32"
SP_DIR = Path(site.getsitepackages()[-1])

FAIL_UNDER = "81"
COV = ["coverage"]
RUN = ["run", "--source=pyproject_fmt", "--branch", "-m"]
PYTEST = ["pytest", "pyproject-fmt/tests", "-vv", "--color=yes", "--tb=long"]
REPORT = ["report", "--show-missing", "--skip-covered", f"--fail-under={FAIL_UNDER}"]

SKIPS = [
    "not-really-a-test-but--k-is-picky",
    "classifier_gt_tox",
]

if WIN:
    SKIPS += [
        "help_invocation_as_script",
        "cli_pyproject_toml_not_file",
    ]

SKIP_OR = " or ".join(SKIPS)
K = ["-k", f"not ({SKIP_OR})"]


def do(*args: Any) -> int:
    """Condition and print arguemnts, return rc."""
    args = [map(str, args)]
    print(">>>", *args, flush=True)
    return call(args)


def check_abi(python_min: str) -> int:
    """Maybe run abi3audit."""
    if not IS_ABI3:
        return True
    ext = "pyd" if WIN else "abi3.so"
    bin = SP_DIR / f"pyproject_fmt/_lib.{ext}"
    return do(["abi3audit", bin, "-s", "-v", f"--assume-minimum-abi3={python_min}"])


if __name__ == "__main__":
    sys.exit(
        check_abi(sys.argv[1])
        # run the tests
        or do([*COV, *RUN, *PYTEST, *K])
        # maybe run coverage
        or do([*COV, *REPORT])
    )
