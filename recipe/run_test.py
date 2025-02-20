import sys
from subprocess import call

WIN = sys.platform == "win32"

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


if __name__ == "__main__":
    sys.exit(
        # run the tests
        call([*COV, *RUN, *PYTEST, *K])
        # maybe run coverage
        or call([*COV, *REPORT])
    )
