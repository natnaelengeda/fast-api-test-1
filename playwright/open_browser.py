import os
import json
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
load_dotenv()

STORAGE_FILE = os.getenv("STORAGE_FILE", "storage.json")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
LOGIN_URL = os.getenv("LOGIN_URL")
POST_LOGIN_SELECTOR = os.getenv("POST_LOGIN_SELECTOR", "selector_that_appears_after_login")  # replace with real selector

def safe_inner_text(element, selector):
    try:
        found = element.query_selector(selector)
        return found.inner_text().strip() if found else ""
    except:
        return ""
    
def login_and_save(context):
    page = context.new_page()
    page.goto(LOGIN_URL)

    page.fill('input[name="email"]', EMAIL)
    page.fill('input[name="password"]', PASSWORD)
    page.click('button[type="submit"]')

    page.wait_for_url("https://djinni.co/jobs/")
    context.storage_state(path=STORAGE_FILE)
    page.close()

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        if os.path.exists(STORAGE_FILE):
            context = browser.new_context(storage_state=STORAGE_FILE)
            print(f"Loaded storage state from {STORAGE_FILE}")
        else:
            context = browser.new_context()
            print("No storage state found, logging in...")
            login_and_save(context)

        page = context.new_page()
        page.goto(LOGIN_URL)

        page.wait_for_selector("li[id^='job-item']")
        first_job = page.query_selector("li[id^='job-item']")

        # experience_years_el = first_job.query_selector("xpath=//span[contains(text(), 'year of experience')]")
        # experience_years = experience_years_el.inner_text().strip() if experience_years_el else ""

        info_items = first_job.query_selector_all("div.fw-medium span.text-nowrap")

        # Default empty values
        work_type = work_place = work_ttype = experience_years = experience_text = ""

        # Fill based on order
        if len(info_items) > 0:
            work_type = info_items[0].inner_text().strip()
        if len(info_items) > 1:
            work_place = info_items[1].inner_text().strip()
        if len(info_items) > 2:
            work_ttype = info_items[2].inner_text().strip()
        if len(info_items) > 3:
            experience_years = info_items[3].inner_text().strip()
        if len(info_items) > 4:
            experience_text = info_items[4].inner_text().strip()
    
        data = {
                "company_name": safe_inner_text(first_job, "a[data-analytics='company_page']"),
                "views": safe_inner_text(first_job, "span:text('views')"),
                "applications": safe_inner_text(first_job, "span:text('applications')"),
                "post_time": safe_inner_text(first_job, "span[data-original-title]"),
                "job_title": safe_inner_text(first_job, "a.job-item__title-link"),
                "work_type": work_type,
                "work_place": work_place,
                "work_ttype": work_ttype,
                "experience_years": experience_years,
                "experience_text": experience_text,
                "primary_content": safe_inner_text(first_job, ".js-truncated-text"),
                }
        
        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(data)

        input("")    
        browser.close()

if __name__ == "__main__":
    main()
