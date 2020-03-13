import shutil
from pprint import pprint

import nox


@nox.session(python=["3.7", "3.8"])
def coverage(session):
    session.install("coverage>=5.0.0")
    session.install("-e", ".[optional]")
    session.install("pytest", "pytest-cov")
    session.run(
        "pytest",
        "--cov=src",
        "--cov-append",
        "--cov-config",
        ".coveragerc",
        "--cov-report",
        "term-missing:skip-covered",
    )
    session.notify("coverage_report")


@nox.session
def coverage_report(session):
    session.install("coverage>=5.0.0")
    session.run("coverage", "html")
    session.notify("coverage_erase")
    session.run("coverage", "report", "--show-missing")
    # TODO: "--fail-under=100"


@nox.session
def coverage_erase(session):
    session.install("coverage")
    session.run("coverage", "erase")


FILES = [
    "src",
    "tests",
    "noxfile.py",
    "noxfile-lint.py",
    "setup.py",
    "docssrc/source/conf.py",
]


@nox.session
def hint(session):
    session.install("isort", "black")
    # session.run('yapf', '--in-place', '--recursive', *FILES)
    session.run("black", *FILES)
    session.run("isort", "--recursive", *FILES)


@nox.session
def lint(session):
    session.install("nox", "vox", "check-manifest")
    # session.run("check-manifest")

    # Delete NOXSESSION so vox can run on CI.
    session.env.pop("NOXSESSION", None)
    session.run("nox", "-r", "-f", "noxfile-lint.py", "--", *session.posargs)

    # python setup.py check --strict --metadata
    # mypy src/dice_stats --config-file tox.ini
    # mypy tests --config-file tox.ini
    # prospector src/ --profile prospector.yaml
    # prospector tests/ --profile prospector-tests.yaml
    # prospector --profile prospector-docstrings.yaml


DOCS = "sphinx", "sphinx_rtd_theme", "sphinx-autodoc-typehints"


def docs_command(builder):
    return [
        "sphinx-build",
        "-b",
        builder,
        "docssrc/source",
        "docssrc/build/_build/{}".format(builder),
    ]


@nox.session
def docs(session):
    session.notify("docs_test")
    session.notify("docs_build")


@nox.session(python="3.8")
def docs_test(session):
    session.install(".[optional]", *DOCS)
    shutil.rmtree("docssrc/build/", ignore_errors=True)
    session.run("pytest", "docssrc/source/")
    session.run(*docs_command("doctest"))
    session.run(*docs_command("linkcheck"))
    session.run(*docs_command("html"))
    shutil.rmtree("docssrc/build/", ignore_errors=True)


@nox.session(python="3.8")
def docs_build(session):
    session.install(".[optional]", *DOCS)
    shutil.rmtree("docs/", ignore_errors=True)
    session.run("sphinx-build", "-b", "html", "docssrc/source", "docs", "-a")
