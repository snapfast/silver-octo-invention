from os import path
from sys import argv

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from time import sleep

home_directory = path.expanduser("~")
local_bin_directory = home_directory + "/bin/"


class LinkedinBot:

    def __init__(self):
        self.page_number = 1
        chrome_options = Options()
        chrome_options.add_argument(
            f"--user-data-dir={local_bin_directory}/chrome-data"
        )
        chrome_options.add_experimental_option("useAutomationExtension", False)

        service = Service()

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://www.linkedin.com/jobs")
        sleep(3)

    def go_exit(self):
        try:
            self.driver.close()
            self.driver.quit()
        except Exception:
            pass

    def do_search(self, position="software engineer", location="germany"):
        try:
            boxes = self.driver.find_elements(
                by=By.CLASS_NAME, value="jobs-search-box__text-input"
            )
            if boxes:
                boxes[0].click()
                sleep(1)
                boxes[0].send_keys(position + "\n")
                sleep(3)

            # Turn on Easy Apply filter if present
            filter_selectors = [
                (By.CLASS_NAME, "search-reusables__filter-binary-toggle"),
                (By.XPATH, "//button[contains(@aria-label, 'Easy Apply filter')]"),
                (By.XPATH, "//button[contains(span/text(), 'Easy Apply')]"),
            ]
            for by, val in filter_selectors:
                try:
                    elem = self.driver.find_element(by=by, value=val)
                    btn = elem if elem.tag_name == "button" else elem.find_element(By.TAG_NAME, "button")
                    btn.click()
                    print("Toggled Easy Apply filter")
                    break
                except Exception:
                    continue
            sleep(3)
        except Exception as e:
            print("Error during job search setup:", e)

    def change_page(self):
        self.page_number += 1
        try:
            selectors = [
                f"//li[@data-test-pagination-page-btn='{self.page_number}']//button",
                f"//button[@aria-label='Page {self.page_number}']",
                f"//button[span[text()='{self.page_number}']]",
            ]
            next_page_button = None
            for selector in selectors:
                buttons = self.driver.find_elements(by=By.XPATH, value=selector)
                if buttons:
                    next_page_button = buttons[0]
                    break

            if next_page_button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                sleep(1)
                next_page_button.click()
                print(f"Navigated to page {self.page_number}")
            else:
                print(f"Could not find button for page {self.page_number}")
        except Exception as e:
            print("Pagination exception:", e)

    def click_easy_jobs(self):
        while True:
            left_panel_jobs = []
            selectors = [
                (By.CLASS_NAME, "scaffold-layout__list-item"),
                (By.CLASS_NAME, "jobs-search-results__list-item"),
                (By.XPATH, "//li[contains(@class, 'job-card-container') or contains(@class, 'jobs-search-results__list-item') or contains(@class, 'scaffold-layout__list-item')]"),
            ]

            for by, val in selectors:
                try:
                    found = self.driver.find_elements(by=by, value=val)
                    if found:
                        left_panel_jobs = found
                        break
                except NoSuchElementException:
                    continue

            total_jobs = len(left_panel_jobs)
            print(f"Found {total_jobs} jobs on page {self.page_number}")

            if total_jobs == 0:
                print("No more jobs found on this page.")
                break

            original_window = self.driver.current_window_handle
            j = 0

            while j < total_jobs:
                sleep(2)
                # Re-fetch list items in case DOM refreshed
                for by, val in selectors:
                    try:
                        found = self.driver.find_elements(by=by, value=val)
                        if found and len(found) > j:
                            left_panel_jobs = found
                            break
                    except Exception:
                        pass

                job_item = left_panel_jobs[j]

                try:
                    title_selectors = [
                        (By.CLASS_NAME, "job-card-list__title--link"),
                        (By.CLASS_NAME, "job-card-list__title"),
                        (By.XPATH, ".//a[contains(@class, 'job-card-list__title')]"),
                    ]

                    job_name_element = None
                    for by, val in title_selectors:
                        try:
                            job_name_element = job_item.find_element(by=by, value=val)
                            if job_name_element:
                                break
                        except NoSuchElementException:
                            continue

                    if not job_name_element:
                        print(f"Could not locate job title for item {j}, skipping.")
                        j += 1
                        continue

                    jname = job_name_element.text or "Unknown Job"
                    job_url = job_name_element.get_attribute("href")

                    if not job_url:
                        print(f"No URL for job {jname}, skipping.")
                        j += 1
                        continue

                    try:
                        with open("filename.txt", "a", encoding="utf-8") as f:
                            print(jname, file=f)
                    except Exception:
                        pass

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job_item)
                    sleep(1)

                    # Open job details in new tab safely
                    self.driver.switch_to.new_window("tab")
                    new_window = self.driver.window_handles[-1]
                    self.driver.switch_to.window(new_window)

                    try:
                        self.driver.get(job_url)
                        sleep(3)
                        self.apply_job()
                        print(f"Finished applying for job: {jname}")
                    finally:
                        try:
                            if len(self.driver.window_handles) > 1 and self.driver.current_window_handle != original_window:
                                self.driver.close()
                        except Exception:
                            pass
                        self.driver.switch_to.window(original_window)

                    j += 1
                except (ElementNotInteractableException, ElementClickInterceptedException):
                    print("Scroll a bit please, cannot interact with element yet.")
                    sleep(2)
                    j += 1
                except Exception as e:
                    print(f"Unexpected error processing job index {j}: {e}")
                    j += 1

            self.change_page()

    def apply_job(self):
        # Section to click the Easy Apply Button on job page
        easy_apply_clicked = False
        apply_selectors = [
            "//button[contains(@class, 'jobs-apply-button')]",
            "//button[contains(@aria-label, 'Easy Apply')]",
            "//button[span[text()='Easy Apply']]",
        ]

        for selector in apply_selectors:
            try:
                buttons = self.driver.find_elements(by=By.XPATH, value=selector)
                for btn in buttons:
                    if btn.is_displayed() and btn.is_enabled():
                        btn.click()
                        print("Clicked the Easy Apply Button")
                        easy_apply_clicked = True
                        break
                if easy_apply_clicked:
                    break
            except Exception as e:
                print(f"Error clicking apply button: {e}")

        if not easy_apply_clicked:
            print("Cannot find or click Easy Apply button, skipping job.")
            return

        sleep(2)

        steps_left = 10
        while steps_left > 0:
            steps_left -= 1

            # Check if resume selection button exists
            try:
                resume_buttons = self.driver.find_elements(
                    by=By.XPATH,
                    value="//button[contains(@class, 'artdeco-button') and (text()='Choose' or span[text()='Choose'])]",
                )
                for rb in resume_buttons:
                    if rb.is_displayed():
                        rb.click()
                        print("Resume button clicked")
                        sleep(1)
                        break
            except Exception:
                pass

            # Try clicking Next, Review, or Submit buttons
            action_clicked = False
            action_selectors = [
                "//button[contains(@class, 'artdeco-button--primary') and (span[text()='Submit application'] or span[text()='Review'] or span[text()='Next'])]",
                "//button[contains(@class, 'artdeco-button--primary') and (text()='Submit application' or text()='Review' or text()='Next')]",
                "//button[@data-easy-apply-next-button]",
            ]

            for selector in action_selectors:
                try:
                    buttons = self.driver.find_elements(by=By.XPATH, value=selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            print(f"Clicked flow button (steps remaining: {steps_left})")
                            action_clicked = True
                            sleep(2)
                            break
                    if action_clicked:
                        break
                except Exception:
                    continue

            if not action_clicked:
                # Modal might have closed or submitted
                print("No further action buttons found or modal closed.")
                break

        print("Job application step finished.")


if __name__ == "__main__":
    position = argv[1] if len(argv) > 1 else "software engineer"
    location = argv[2] if len(argv) > 2 else "germany"

    lb = LinkedinBot()
    lb.do_search(position, location)
    lb.click_easy_jobs()
