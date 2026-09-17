import os
import sqlite3
import yaml
from flask import Flask, request

app = Flask(__name__)

# --- Hardcoded credentials (fake/example values, for secret-scan testing) ---
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def get_user(username):
    """SQL Injection: string-concatenated query. CodeQL should flag this."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()


@app.route("/user")
def user_lookup():
    username = request.args.get("username", "")
    return str(get_user(username))


@app.route("/run")
def run_command():
    """Command Injection: unsanitized input to os.system. CodeQL should flag this."""
    cmd = request.args.get("cmd", "")
    os.system(cmd)
    return "executed"


@app.route("/calc")
def calculate():
    """Code Injection: eval() on user input. CodeQL should flag this."""
    expression = request.args.get("expr", "0")
    result = eval(expression)
    return str(result)


@app.route("/config", methods=["POST"])
def load_config():
    """Insecure Deserialization: unsafe yaml.load. CodeQL should flag this."""
    data = request.data
    config = yaml.load(data, Loader=yaml.Loader)
    return str(config)


if __name__ == "__main__":
    # debug=True in production is itself a CodeQL finding.
    app.run(debug=True)
