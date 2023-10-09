import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import List

op = Options()
op.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
op.add_argument("--headless=new")

class Parser:
    default_url = 'https://ya.ru/search/?text='

    def __init__(self, company_name: str, queries: List[str], page_size=1, url=default_url):
        self.url = url
        self.company_name = company_name
        self.queries = queries
        self.page_size = page_size - 1
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=op)

    def parser(self):
        response = []
        page_size = self.page_size
        try:
            for query in self.queries:
                if page_size == 0:
                    self.driver.get(f'{self.url}{self.company_name}+{query}&p={self.page_size}')
                    page = self.__parse_page(self.driver.page_source)
                    response.append({query: page})
                elif page_size == 1:
                    arr = []
                    for i in range(0, page_size):
                        self.driver.get(f'{self.url}{self.company_name}+{query}&p={i}')
                        page = self.__parse_page(self.driver.page_source)
                        arr.extend(page)
                        response.append({query: page})
        except ExceptionGroup as e:
            date = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
            self.driver.save_screenshot(f"screenshot_{date}.png")
            print(e)
        finally:
            self.driver.close()
            self.driver.quit()
        return response



    def __parse_page(self, source):
        if source:
            soup = BeautifulSoup(source, 'html.parser')
            time.sleep(1)

            search_result = soup.find('ul', {'id': 'search-result'})

            blocks = search_result.findAll('li')

            result = []
            if len(blocks):
                for block in blocks:
                    find_href = block.find('a')
                    find_title = block.find('h2')
                    find_label = block.find('label')

                    if find_href.has_attr('href') and find_title and find_label:
                        if len(find_title.findAll('b')) > 1 or len(find_label.findAll('b')) > 1:
                            result.append(
                                {
                                    "title": find_title.get_text(),
                                    "link": find_href['href'],
                                }
                            )

            return result
        else:
            return []
