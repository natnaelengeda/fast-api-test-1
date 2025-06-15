from anticaptchaofficial.recaptchav2 import *

def solve_recaptcha(site_key, page_url, api_key):
    solver = recaptchaV2()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(page_url)
    solver.set_website_key(site_key)

    token = solver.solve_and_return_solution()
    if token != 0:
        print("CAPTCHA solved:", token)
        return token
    else:
        print("Failed to solve CAPTCHA:", solver.error_code)
        return None
