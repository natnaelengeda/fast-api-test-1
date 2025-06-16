import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

DATA_FILE = Path("all_jobs.json")
OUTPUT_FILE = Path("all_jobs_eligible.json")

def check_eligibility(page):
    ul = page.query_selector("aside ul.list-unstyled")
    if not ul:
        return False
    li_items = ul.query_selector_all("li")
    for li in li_items:
        # look for danger icons
        icon = li.query_selector("span.bi.bi-x-circle.text-danger")
        if icon:
            return False
    return True

def run_eligibility_check():
    jobs = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        browser_context = browser.new_context(storage_state="storage.json")
        page = browser_context.new_page()

        for i, job in enumerate(jobs, 1):
            print(f"[{i}/{len(jobs)}] Checking eligibility for: {job['job_title']}")
            page.goto(job["job_link"])

            time.sleep(3)
            page.keyboard.press("PageDown")
            time.sleep(1)

            job["eligible"] = check_eligibility(page)
            print(f" ➤ Eligible: {job['eligible']}")

        browser.close()

    OUTPUT_FILE.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Done! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_eligibility_check()
