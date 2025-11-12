# 🧪 epr-data-automation

A **Playwright + Python** automation framework for **data setup** and **data validation** across UI, ETL, and DB layers.

This framework provides:

- 🧰 **Command Line Utilities** — for creating and managing end-to-end data setups:
  - Direct Producer: enrolment, registration submission, POM submission
  - Direct Producer + Subsidiaries: registration submission, POM submission
  - Compliance Scheme: enrolment, registration submission, POM submission
  - Compliance Scheme + Subsidiaries: enrolment, registration submission, POM submission

- 🧪 **Data Validation Functional Tests**
- ✅ **Multi-environment support** (dev15, tst1, tst2, preprod…)

---

## ✅ Example Data Validation Flow — *Joiners Report*

1️⃣ Create the data setup using utilities:  
- direct producer enrolment  
- create subsidiaries  
- perform registration submission  

2️⃣ Trigger the ETL pipeline

3️⃣ Validate populated Joiners Report tables

---

## ⚙️ Tech Stack

- **Python 3.10.10+**
- **Playwright** (UI automation)
- **VS Code** (recommended editor)
- **asdf** (Python version manager)
- **direnv** (per-project virtualenv + `PYTHONPATH`)
- **uv** (dependency & environment manager)
- **Ruff** (linting + formatting)
- **Mypy** (optional static type checking)

---

## 🚀 Setup

### 1️⃣ Install prerequisites

```bash
brew install asdf direnv uv
```

Add shell hooks (example for Fish):

```fish
# ~/.config/fish/config.fish
source /opt/homebrew/opt/asdf/libexec/asdf.fish
eval (direnv hook fish)
```

Reload shell:

```bash
exec fish
```

---

### 2️⃣ Allow direnv in project root

```bash
direnv allow
```

---

### 3️⃣ Run project setup

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This installs:
- uv-managed dependencies  
- Playwright browsers  
- Ruff + Mypy  
- Compiled requirements.txt  

---

## 🧰 Command Line Utilities

### ✅ Direct Producer Enrolment

```bash
python -m eprda.cli.dp_enrolment
```

### ✅ Direct Producer Registration Submission

```bash
python -m eprda.cli.dp_registration_submission
```

Use a specific environment profile:

```bash
ENV_PROFILE=tst1 python -m eprda.cli.dp_enrolment
```

Defaults to **dev15** if not provided.

---

## 🧪 Running Tests

```bash
pytest
```

Run in a specific environment:

```bash
ENV_PROFILE=tst1 pytest
```

PyTest auto-loads:

```
config/environments/.env.<profile>
```

---

## 📁 Project Structure

```text
epr-data-automation/
├─ config/                       # Project config files (resources only)
│  └─ environments/              # .env.<profile> environment files
│       ├── .env.dev15
│       ├── .env.tst1
│       ├── .env.tst2
│       └── .env.preprod
│
├─ output/                       # Generated CSVs and run artifacts
│
├─ templates/                    # CSV templates (org/POM file structures)
│
├─ scripts/
│   └── setup.sh                 # First-time setup script
│
├─ src/
│  └─ eprda/                     # Main Python package
│     ├─ cli/                    # Command Line utilities
│     ├─ clients/                # API/DB/ETL clients
│     ├─ config/                 # Environment & secrets loader code
│     │   ├─ env_loader.py
│     │   └─ settings.py
│     ├─ flows/                  # Business flows (UI + API orchestration)
│     ├─ ui/                     # Playwright layer
│     │   ├─ browser.py          # Browser bootstrap
│     │   └─ pages/              # Page Object Models
│     └─ utils/                  # CSV factory + other utilities
│
├─ tests/
│  ├─ conftest.py                # Global fixtures & environment boot
│  ├─ data/                      # Data validation tests
│  ├─ ui/                        # UI test suites
│  └─ api/                       # API tests
│
├─ pyproject.toml                # Tooling: Ruff, MyPy, PyTest, build config
├─ requirements.txt              # uv-compiled pinned dependencies
└─ README.md
```

---

## 🔧 Common Commands

```bash
# Lint & auto-fix
ruff check . --fix

# Format
ruff format .

# Update dependencies
uv pip compile pyproject.toml -o requirements.txt
uv pip sync requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps
```

---

## 📝 Environment Profiles

All environment files live here:

```
config/environments/.env.<profile>
```

Examples:

```
.env.dev15
.env.tst1
.env.tst2
.env.preprod
```

Set profile for CLI/tests:

```bash
ENV_PROFILE=tst1
```

Defaults to `dev15` if not supplied.

---

🎉 **Happy testing and automation!**
