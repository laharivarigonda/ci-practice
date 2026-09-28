# CI Practice: Python Calculator

This project demonstrates continuous integration (CI) with Python, pytest, Ruff, and GitHub Actions. Every push to `main` runs lint checks and tests automatically on GitHub.

The calculator supports addition, subtraction, multiplication, and division. The steps below describe how to build this project from scratch using Windows PowerShell.

## 1. Prerequisites

Install Python 3.11 and Git, and create a GitHub account. Check your installations:

```powershell
python --version
git --version
```

## 2. Create the project folder

```powershell
mkdir ci-practice
cd ci-practice
```

If you already have this project open, use its existing folder and skip this step.

The completed project has this structure:

```text
ci-practice/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── calculator.py
├── test_calculator.py
├── requirements.txt
└── README.md
```

## 3. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

The terminal prompt should now begin with `(venv)`. Activate the environment again whenever you open a new terminal to work on this project.

## 4. Add and install dependencies

Create `requirements.txt` with:

```text
pytest
ruff
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

- **pytest** runs the automated tests.
- **Ruff** checks Python code for lint errors.

## 5. Write the calculator functions

Create `calculator.py`:

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def division(a, b):
    return a / b
```

Division uses Python's normal `/` behavior: it returns a floating-point result for integer inputs and raises `ZeroDivisionError` if the divisor is zero.

## 6. Write automated tests

Create `test_calculator.py`:

```python
from calculator import add, division, multiply, subtract


def test_add():
    assert add(2, 3) == 5


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(4, 3) == 12


def test_division():
    assert division(20, 2) == 10
```

pytest discovers files and functions named `test_*`. Each assertion compares the actual result with the expected result. These four tests cover one example for each operation.

## 7. Run checks locally

Run the lint check and tests before committing:

```powershell
python -m ruff check .
python -m pytest
```

With the current code, Ruff reports `All checks passed!` and pytest reports `4 passed`.

To explicitly check import ordering as well:

```powershell
python -m ruff check --select I .
```

The current workflow uses `ruff check .` without a Ruff configuration file. Import-sorting rules (`I`) are not enabled by default; the explicit command above checks them separately.

## 8. Ignore generated files

Create `.gitignore`:

```gitignore
venv/
__pycache__/
.pytest_cache/
```

These entries keep the virtual environment, Python bytecode cache, and pytest cache out of new Git commits. They may still appear on your computer; that is normal. Ignore rules do not remove files that Git already tracks.

## 9. Create the GitHub Actions workflow

Create the workflow folder:

```powershell
New-Item -ItemType Directory -Path .github/workflows -Force
```

Create `.github/workflows/ci.yml` with the following content. Use spaces for YAML indentation:

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run lint
        run: ruff check .

      - name: Run tests
        run: pytest
```

When a commit is pushed to `main`, GitHub starts an Ubuntu runner, checks out the repository, sets up Python 3.11, installs dependencies, runs Ruff, and then runs pytest. If a step fails, the job fails and later steps are normally skipped.

This workflow runs on pushes to `main`. It does not currently define pull request or manual triggers, or a deployment step.

## 10. Initialize Git and commit the project

For a new project that is not already a Git repository:

```powershell
git init
git add .
git commit -m "Initial CI practice project"
git branch -M main
```

If Git asks for your identity, configure it for this repository using your own details, then retry the commit:

```powershell
git config user.name "Your Name"
git config user.email "your-email@example.com"
```

## 11. Connect to GitHub and push

Create a repository named `ci-practice` on GitHub. For this from-scratch process, leave it empty: do not initialize it with a README, license, or `.gitignore`, because those files are being created locally.

Connect the local repository and push. Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/ci-practice.git
git push -u origin main
```

For this project, the remote is `https://github.com/laharivarigonda/ci-practice`. If `origin` already exists, inspect it with `git remote -v` instead of adding it again.

The `-u` option sets the upstream branch, so future pushes can use `git push`.

## 12. Check the CI result

1. Open the repository on GitHub.
2. Select the **Actions** tab.
3. Open the latest **CI Pipeline** run.
4. Open the `test` job and inspect the installation, lint, and test steps.
5. A green check means the workflow passed. If it fails, expand the failed step to read the error.

## 13. Make changes and rerun CI

After editing the calculator or its tests, run:

```powershell
python -m ruff check .
python -m pytest
git status
git add calculator.py test_calculator.py
git commit -m "Update calculator and tests"
git push
```

Stage other files explicitly when you change them, such as `README.md` or `.github/workflows/ci.yml`. Each push to `main` starts another CI run.

For a practice failure, temporarily change an expected result in a test and run pytest locally. Restore the correct assertion and rerun pytest to see it pass. To observe the same failure on GitHub, commit and push the failing test, then commit and push the correction.

## Troubleshooting from this project

### GitHub rejects your username or token

GitHub does not accept an account password for HTTPS Git operations. With Git Credential Manager installed, sign in again through the browser:

```powershell
git credential-manager github login --username YOUR_USERNAME --browser --force
```

Complete the browser authentication with the account that has access to the repository, then retry:

```powershell
git push -u origin main
```

### Push rejected with “fetch first”

This means the remote has commits that your local branch does not contain. Start with a clean working tree, then fetch and inspect both histories:

```powershell
git fetch origin
git log --oneline --graph --all
```

For branches with shared history, merge the remote changes and push:

```powershell
git merge origin/main
git push -u origin main
```

In this project, GitHub had a separate initial README commit and the local project had its own initial commit. Because those histories were unrelated, the fix was:

```powershell
git merge origin/main --allow-unrelated-histories -m "Merge remote README with local project"
git push -u origin main
```

Use `--allow-unrelated-histories` only when you intentionally want to combine two independently initialized histories. If Git reports conflicts, edit the affected files to retain the desired content, remove conflict markers, stage the resolved files, and commit before pushing. A force push is not needed for this fix.

### Ruff reports `I001`: imports are unsorted

Sort the imported names:

```python
from calculator import add, division, multiply, subtract
```

You can also apply the import-order fix automatically and review the change:

```powershell
python -m ruff check --select I --fix test_calculator.py
git diff
```

An `I001` error means import-sorting rules were enabled for that run. To enforce those rules in this project's CI, change its lint command to `ruff check --extend-select I .`.

### pytest reports `SyntaxError: expected ':'`

Every Python function definition needs a trailing colon. The division function must start with:

```python
def division(a, b):
    return a / b
```

A syntax error prevents pytest from importing the module and collecting its tests. Fix the syntax, then rerun the checks:

```powershell
python -m ruff check .
python -m pytest
```

### Local checks pass, but GitHub still shows a failed run

Local edits do not change an existing GitHub Actions run. Save the files, commit and push the fix, then inspect the newest run for that commit. Check that your local Python version and installed dependencies match the workflow if the latest run still fails.
