# vulnerable-python-demo

Deliberately vulnerable Flask app, for testing the `github-platform-workflows`
reusable pipeline: build, unit test, CodeQL analysis, dependency review, and
secret scanning.

**Do not deploy this app anywhere real — it is intentionally insecure.**

## What's deliberately broken (and why)

| File | Issue | Should be caught by |
|---|---|---|
| `app.py` | SQL injection in `get_user()` | CodeQL |
| `app.py` | Command injection in `run_command()` | CodeQL |
| `app.py` | `eval()` on user input in `calculate()` | CodeQL |
| `app.py` | Unsafe `yaml.load()` in `load_config()` | CodeQL |
| `app.py` | `debug=True` in Flask app | CodeQL |
| `app.py` | Hardcoded AWS-style credentials (fake/example values) | Secret scanning / Gitleaks |
| `requirements.txt` | Old `Flask`, `requests`, `PyYAML` versions with known CVEs | Dependabot / Dependency review |

## Setup

1. Create this repo on GitHub, e.g. `github.com/<your-username>/vulnerable-python-demo`.
2. Push all these files.
3. The workflow references the shared `kprasadpn/github-platform-workflows`
   repository. If you use a fork of that repository, update the composite
   action references in `.github/workflows/main.yml` to point to your fork.
4. Enable, under `Settings -> Security -> Code security and analysis`:
   - Dependency graph
   - Dependabot alerts
   - Dependabot security updates
   - Secret scanning (if available on your plan/repo visibility)
   - Code scanning (this gets populated by the CodeQL workflow itself)
5. Push a commit or open a PR — the pipeline in `main.yml` will call out to
   `github-platform-workflows` for each CI stage. Build, unit tests, and CodeQL
   now run in one job so CodeQL initialization and analysis share the same
   checkout and build context; dependency review and secret scanning remain
   separate checks.

## Expected results after first run

- **Actions tab**: build + unit-test jobs pass; CodeQL analyze job runs and
  uploads results to the Security tab.
- **Security -> Code scanning alerts**: SQL injection, command injection,
  eval injection, unsafe deserialization, Flask debug mode.
- **Security -> Secret scanning alerts**: the fake AWS key pair in `app.py`.
- **Security -> Dependabot alerts**: CVEs for the pinned old package versions.
- **Pull requests**: opening a PR triggers `dependency-review`, which will
  flag/fail on the vulnerable dependencies depending on the severity
  threshold set.
