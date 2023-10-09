from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from typing import List
import time


class Parser:
    url = 'https://ya.ru/search/?text='

    def __init__(self, company_name: str, queries: List[str], url=url):
        self.url = url
        self.company_name = company_name
        self.queries = queries
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()));

    def parser(self):
        try:
            self.driver.get(f'{self.url}{self.company_name}{self.queries}')
            time.sleep(5000)

            body = self.driver.find_element(by=By.ID, value='search-result')
            soup = BeautifulSoup(body.text, 'html.parser')
            lt = soup.find('b', self.company_name).prettify()
            return lt

        except Exception as e:
            print(e)
