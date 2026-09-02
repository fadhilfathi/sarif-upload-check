"""Deliberately flawed sample. Exists only as a target for SARIF locations.

Not a library, not installed, not run. The lines below are referenced by
sarif/emitted.sarif so uploaded alerts land somewhere real.
"""

import os
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/run")
def run_command():
    cmd = request.args.get("cmd", "")
    return subprocess.check_output(cmd, shell=True)


@app.route("/user")
def lookup_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    return conn.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()


@app.route("/read")
def read_file():
    path = request.args.get("path", "")
    with open(os.path.join("/data", path)) as handle:
        return handle.read()


def already_reviewed_by_a_human():
    """Referenced by the result that arrives already suppressed."""
    return subprocess.check_output(["ls", "-la"])


def suppressed_in_source():
    """Referenced by the result suppressed with kind "inSource"."""
    return subprocess.check_output(["pwd"])  # nosem
