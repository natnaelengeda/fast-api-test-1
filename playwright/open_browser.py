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
        browser = p.chromium.launch(headless=True)

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
        
        job_elements = page.query_selector_all("li[id^='job-item']")

        all_jobs = []

        for job in job_elements:
            info_items = job.query_selector_all("div.fw-medium span.text-nowrap")

            work_type = work_place = work_ttype = experience_years = experience_text = ""

            link = job.query_selector("a.job-item__title-link")
            href = link.get_attribute("href") if link else ""
            full_url = f"https://djinni.co{href}" if href else ""

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
                "company_name": safe_inner_text(job, "a[data-analytics='company_page']"),
                # "company_profile": safe_inner_text(job, "a[]"),
                "views": safe_inner_text(job, "span:text('views')"),
                "applications": safe_inner_text(job, "span:text('applications')"),
                "post_time": safe_inner_text(job, "span[data-original-title]"),
                "job_title": safe_inner_text(job, "a.job-item__title-link"),
                "job_link": full_url,
                "work_type": work_type,
                "work_place": work_place,
                "work_ttype": work_ttype,
                "experience_years": experience_years,
                "experience_text": experience_text,
                "primary_content": safe_inner_text(job, ".js-truncated-text"),
            }

            all_jobs.append(data)
        
        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump(all_jobs, f, ensure_ascii=False, indent=2)

        print(data)

        # input("")    
        browser.close()

if __name__ == "__main__":
    main()
