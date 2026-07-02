# AutoMates

AutoMates is a Python-based automation tool to help you streamline your job application process on major job portals like LinkedIn, Naukri, and Wellfound using Selenium.

Not Updating the code, fixes are welcome. I will try to merge your code as early as possible.

## Prerequisites

- **Python 3.10 and above**
- **Google Chrome** installed on your system.

## Setup (Ubuntu / General)

Run the following commands to clone the repository and install the required `selenium` package.

```bash
git clone https://github.com/snapfast/AutoMates
cd AutoMates
pip install selenium
python run.py
```

Just follow the interactive menu to select the job site and automate the tasks.

### Note on WebDrivers

**Selenium Manager**: Since the release of Selenium Manager, browsers like Chrome, Firefox, and Safari drivers are automatically configured by Selenium. You do not need to manually download or specify the `chromedriver` path.
Read more here: https://www.selenium.dev/blog/2022/introducing-selenium-manager/

## Usage

When you run `python run.py` for the first time, you will be prompted to login:
1. Select the option to let the script open a Chrome window for you.
2. You will have two minutes to manually log in to the job sites (LinkedIn, Naukri, etc.).
3. Once logged in, the script saves your session data locally so you don't have to log in again in subsequent runs.

Choose the service to automate:
1. **WellFound**: Automate connection requests.
2. **LinkedIn**:
    - Apply to LinkedIn Recommended Jobs.
    - Search jobs based on Position and Location, and apply to Easy Apply jobs.
    - Connect to people at specific companies.
    - Stalk profiles to increase profile views.
    - Connect to recruiters hiring for certain positions.
3. **Naukri**: Apply to Naukri Recommended Jobs.

## Points to Note

- There is no automatic upload feature yet; resumes or cover letter files should be manually pre-uploaded to the job portals beforehand.
- If you encounter issues, please raise an issue on GitHub.
- For adding new features or ideas, open a new issue [here](https://github.com/snapfast/AutoMates/issues/new).
