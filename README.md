# AutoMates

AutoMates is a powerful, interactive Python-based automation tool built with Selenium to streamline and accelerate your job application process on major job portals.

> **Note:** AutoMates currently targets automation for **LinkedIn** and **Naukri**, with support for saving browser session data locally so you don't have to log in repeatedly.

---

## Key Features

### 1. LinkedIn Automation (`LINKEDIN/`)
- **Recommended Jobs**: Automatically find and apply to LinkedIn's Recommended Jobs using "Easy Apply".
- **Custom Job Search & Apply**: Search for specific positions and locations, then automate "Easy Apply" submissions.
- **Network Expander**: Send targeted connection requests to people working at specified companies.
- **Profile Stalker**: Systematically visit relevant profiles to increase your own profile visibility and views.
- **Recruiter Connector**: Search for recruiters hiring for specific positions and send them personalized connection messages.

### 2. Naukri Automation (`NAUKRI/`)
- **Recommended Jobs**: Automatically apply to job postings on your Naukri Recommended Jobs feed.

### 3. Session Persistence
- **One-time Login**: The script launches Chrome to let you log in manually. Once logged in, your session data is persisted in a local directory (`~/bin/chrome-data`), eliminating the need to log in during subsequent runs.

---

## Prerequisites

- **Python 3.10 and above**
- **Google Chrome** installed on your system.
- **Selenium Manager**: AutoMates leverages Selenium 4's built-in *Selenium Manager*. It automatically manages the browser drivers (like `chromedriver`) based on your installed Chrome version. **No manual driver installation or path configuration is required.**

---

## Installation & Setup

Follow these simple steps to set up and run AutoMates on your machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/snapfast/AutoMates
   cd AutoMates
   ```

2. **Install Dependencies**:
   ```bash
   python3 -m pip install selenium
   ```

3. **Run the Application**:
   ```bash
   python3 run.py
   ```

---

## How to Use

When you run `python3 run.py`, an interactive command-line interface will guide you through the process:

### Step 1: Initial Login Setup
On your first run, choose option **1**:
```
1. Let me login to the website.
2. I am already logged in previously using this script.
```
- A Chrome window will open.
- You have **two minutes** to log in to your accounts (LinkedIn, Naukri, etc.).
- Once done, close the window or let the timer finish. Your login sessions will be safely stored locally.
- For all subsequent runs, you can choose option **2** to skip the login phase.

### Step 2: Choose Automation Service
Select the service you want to run:
- **`2` for LinkedIn**: Then select from the sub-menu (Recommended jobs, Custom search, Network expander, Profile stalker, or Recruiter connector).
- **`3` for Naukri**: Automatically begins applying to your Recommended Jobs.

---

## Advanced Configuration

### Personalized Recruiter Messages
When using the recruiter connection feature, you can customize the introduction message sent to recruiters.
Edit the candidate info variable in **`LINKEDIN/constants.py`**:
```python
LINKEDIN_CANDIDATE_INFO = """
Hi,
I have a total of 4+ years of experience as full stack engineer.
Build/scale SaaS products from scratch and contributed to many great products.
Resume: [Your Link Here]
Kindly let me know if there are any requirements.
"""
```

### Adjusting Selectors
If job board layouts change, you can update class names and XPaths in **`config.ini`**:
```ini
[RECOMMENDED]
JobCardClassName = "jobs-job-board-list__item"
EasyApplySubtitleClassName = "job-card-container__apply-method"
EasyApplyButtonXPath = "//button[@class='jobs-apply-button artdeco-button artdeco-button--3 artdeco-button--primary ember-view']"
```

---

## Points to Note & Best Practices

- **Resumes & Cover Letters**: Ensure your default resumes/CVs and profile details are pre-uploaded and completed on LinkedIn and Naukri. AutoMates executes the submission click flow but does not upload files dynamically.
- **Account Safety**: Use automation responsibly. Setting excessively fast speeds or running the script constantly may trigger portal rate limits.
- **Contributions**: Contributions, bug fixes, and feature additions are highly welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
