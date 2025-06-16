import json
from playwright.sync_api import sync_playwright

def safe_inner_text(element, selector):
    try:
        target = element.query_selector(selector)
        return target.inner_text().strip() if target else ""
    except:
        return ""
  
def extract_job_data(job):
    info_items = job.query_selector_all("div.fw-medium span.text-nowrap")

    work_type = work_place = work_ttype = experience_years = experience_text = ""
    if len(info_items) > 0: work_type = info_items[0].inner_text().strip()
    if len(info_items) > 1: work_place = info_items[1].inner_text().strip()
    if len(info_items) > 2: work_ttype = info_items[2].inner_text().strip()
    if len(info_items) > 3: experience_years = info_items[3].inner_text().strip()
    if len(info_items) > 4: experience_text = info_items[4].inner_text().strip()

    href = job.query_selector("a.job-item__title-link").get_attribute("href") if job.query_selector("a.job-item__title-link") else ""

    return {
        "company_name": safe_inner_text(job, "a[data-analytics='company_page']"),
        "views": safe_inner_text(job, "span:text('views')"),
        "applications": safe_inner_text(job, "span:text('applications')"),
        "post_time": safe_inner_text(job, "span[data-original-title]"),
        "job_title": safe_inner_text(job, "a.job-item__title-link"),
        "job_link": f"https://djinni.co{href}" if href else "",
        "work_type": work_type,
        "work_place": work_place,
        "work_ttype": work_ttype,
        "experience_years": experience_years,
        "experience_text": experience_text,
        "primary_content": safe_inner_text(job, ".js-truncated-text"),
    }

def get_total_pages(page):
    pagination = page.query_selector_all("ul.pagination li.page-item")
    max_page = 1
    for item in pagination:
        text = item.inner_text().strip()
        if text.isdigit():
            max_page = max(max_page, int(text))
    return max_page

def scrape_djinni_jobs():
    all_jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="storage.json")
        page = context.new_page()

        base_url = "https://djinni.co/jobs/?primary_keyword=react&page="
        page_number = 1

        page.goto(base_url + str(page_number))
        total_pages = get_total_pages(page)
        print(f"Total pages: {total_pages}")

        while page_number <= total_pages:
            print(f"Scraping page {page_number}...")
            page.goto(base_url + str(page_number))

            jobs = page.query_selector_all("li[id^='job-item']")
            for job in jobs:
                all_jobs.append(extract_job_data(job))

            page_number += 1

        browser.close()

    # Save all jobs
    with open("all_jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_djinni_jobs()