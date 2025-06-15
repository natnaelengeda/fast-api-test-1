from playwright.sync_api import sync_playwright
import json

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com/jobs")

        # Replace this with the actual selector for job cards/items
        job_cards = page.locator(".job-card")  

        jobs = []

        count = job_cards.count()
        for i in range(count):
            job = {}
            card = job_cards.nth(i)
            job['title'] = card.locator(".job-title").text_content()
            job['company'] = card.locator(".company-name").text_content()
            job['location'] = card.locator(".location").text_content()
            job['link'] = card.locator("a.job-link").get_attribute("href")
            jobs.append(job)

        browser.close()

        # Format the scraped data as JSON
        print(json.dumps(jobs, indent=2))

if __name__ == "__main__":
    scrape_jobs()
