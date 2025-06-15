from bs4 import BeautifulSoup
import requests


def fetch_web_page(site:str):
  html_document = get_html_document(site)

  soup = BeautifulSoup(html_document, 'html.parser')
  return soup.prettify()


def get_html_document(url):
    response = requests.get(url)

    return response.text