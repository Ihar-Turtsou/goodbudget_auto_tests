# 💸 Goodbudget Auto Tests

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](#)
[![Pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC.svg)](#)
[![Allure](https://img.shields.io/badge/report-Allure-8A2BE2.svg)](#)
[![CI](https://img.shields.io/badge/Jenkins-ready-success.svg)](#)

Automated testing project for **Goodbudget**, covering **UI**, **API**, and **Mobile** layers.  
This repository is structured as a real project with smooth local and CI (Jenkins) execution, **Allure reports**, videos, and browser/emulator logs.

---

## 📚 Table of Contents
- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration & Environment Variables](#-configuration--environment-variables)
- [Running Tests](#-running-tests)
  - [UI: Local / Remote (Selenoid)](#ui-local--remote-selenoid)
  - [API](#api)
  - [Mobile: Local (Appium) / Remote (BrowserStack)](#mobile-local-appium--remote-browserstack)
- [CI/CD (Jenkins)](#-cicd-jenkins)
- [Reports & Attachments](#-reports--attachments)
- [Useful Commands](#-useful-commands)

---

## 🎯 Overview

- **UI tests** — Based on **Selene (Selenium 4)** + **Pytest**, with fixtures and Allure attachments (screenshots, HTML, logs, Selenoid videos).  
- **API tests** — Lightweight client using **requests** for transaction-related endpoints.  
- **Mobile tests** — Built on **Appium**, run locally or on **BrowserStack**, with video attachments to Allure.

---

## 🧰 Tech Stack

| Category | Technologies |
|-----------|---------------|
| Language | Python 3.12+ |
| Framework | Pytest |
| Web UI | Selene 2 (Selenium 4) |
| Mobile | Appium Python Client |
| Reports | Allure (allure-pytest) |
| CI/CD | Jenkins |
| Cloud | Selenoid, BrowserStack |
| Config / ENV | pydantic, python-dotenv |

All required dependencies are listed in `requirements.txt`.

---

## 🗂 Project Structure

```
goodbudget_auto_tests/
├── config.py
├── pytest.ini
├── requirements.txt
├── goodbudget/
│   ├── api/
│   │   ├── client.py
│   │   └── payloads.py
│   ├── mobile/
│   │   └── screens/
│   │       ├── base_screen.py
│   │       ├── home_screen.py
│   │       ├── login_screen.py
│   │       └── onboarding_screen.py
│   └── ui/
│       └── pages/
│           ├── home_page.py
│           ├── login_page.py
│           └── logout_page.py
├── resources/
│   └── apk/
│       └── base.apk
├── tests/
│   ├── conftest.py
│   ├── test_api/
│   ├── test_mobile/
│   │   └── test_android/
│   └── test_ui/
└── utils/
    ├── api_helpers.py
    ├── attach.py
    ├── file_helpers.py
    ├── logger_allure.py
    ├── logger_console.py
    └── schema.py
```

**Pytest markers** are defined in `pytest.ini`:
```
ui, api, mobile, smoke, regression
```

---

## ⚙️ Installation

1. Clone the repository and install dependencies:
```bash 
pip install -r requirements.txt
```

---

## 🔧 Configuration & Environment Variables

Project uses `.env` for secrets and URLs. Create it in the project root (next to `pytest.ini`).

**UI / API:**
```env
GB_BASE_URL=https://goodbudget.com
GB_USERNAME=your_login
GB_PASSWORD=your_password

# API only
HOUSEHOLD_ID=...
ACCOUNT_UUID=...
```

**Selenoid (Remote UI):**
```env
SELENOID_LOGIN=your_selenoid_user
SELENOID_PASS=your_selenoid_pass
SELENOID_URL=selenoid.autotests.cloud
```

**Local Mobile (Appium):**
Defaults from `config.py`:
- `appium_url = http://127.0.0.1:4723`
- `device_name = emulator-5554`
- `app_path = resources/apk/base.apk`

**BrowserStack Mobile:**
```env
BROWSERSTACK_USERNAME=...
BROWSERSTACK_ACCESS_KEY=...
BROWSERSTACK_APP_ID=bs://<uploaded-app-id>
```

> Configs managed via `get_local_config()` and `get_bs_config()` (pydantic).

---

## 🚀 Running Tests

### UI: Local / Remote (Selenoid)

**Local (default Chrome):**
```bash
pytest -m ui --local
```

**Remote (Selenoid):**
```bash
pytest -m ui
```
The `setup_browser` fixture automatically switches based on `--local` flag and attaches screenshots, logs, HTML, and **video** to Allure.

### API

```bash
pytest -m api
```

### Mobile: Local (Appium) / Remote (BrowserStack)

**Local (emulator / real device):**
```bash
# Make sure Appium server is running
appium --address 0.0.0.0 --port 4723
pytest -m mobile --local
```

**Remote (BrowserStack):**
```bash
pytest -m mobile
```

- Local mode uses `get_local_config()` → attaches local video to Allure.  
- BrowserStack mode uses `get_bs_config()` → attaches **session video** via `attach_bs_video(session_id)`.

---

## 🔄 CI/CD (Jenkins)

### ⚙️ Run tests in Jenkins

1. Log in to **Jenkins**  
2. Select the job **`goodbudget_graduation_project_ihar-t`**  
3. Click **Build Now**  
4. After the run finishes, open the **Allure Report** or **Allure TestOps**  icon on the build page

![Jenkins_build_page](./resources/images/screenshots/jenkins_build.png)


---

## 📊 Reports & Attachments

Pytest is pre-configured in `pytest.ini`:
```ini
addopts = --clean-alluredir --alluredir=allure-results
```

**To view the report (local run):**
```bash
allure serve allure-results
```

Allure report includes:
- Screenshots, page source, browser logs
- Selenoid videos (UI)
- Local / BrowserStack videos (Mobile)

### Allure Report
![Allure Report](./resources/images/screenshots/allure_example.png)

### Allure TestOps
![Allure TestOps](./resources/images/screenshots/allure_testops.png)

### Telegram Notifications
![Telegram report](./resources/images/screenshots/telegram_example.png)


---

## 🧾 Useful Commands

```bash
# Install & run
pip install -r requirements.txt
pytest -m smoke
pytest -m regression

# By groups
pytest -m ui
pytest -m api
pytest -m mobile

# Local modes
pytest -m ui --local
pytest -m mobile --local

```


