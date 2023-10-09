from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import List

op = Options()
op.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})

class Parser:
    url = 'https://ya.ru/search/?text='

    def __init__(self, company_name: str, queries: List[str], url=url):
        self.url = url
        self.company_name = company_name
        self.queries = queries
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=op)

    def parser(self):
        response = []
        self.driver.get(f'{self.url}{self.company_name}')
        self.driver.delete_all_cookies()

        try:
            for query in self.queries:
                self.driver.get(f'{self.url}{self.company_name}+{query}')
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                search_result = soup.find('ul', {'id': 'search-result'})
                blocks = search_result.findAll('li')

                result = []
                if len(blocks):
                    for block in blocks:
                        find_href = block.find('a')['href']
                        find_title = block.find('h2')
                        find_label = block.find('label')

                        if find_href and find_title and find_label:
                            if len(find_title.findAll('b')) > 1 or len(find_label.findAll('b')) > 1:
                                result.append(
                                    {
                                        "title": find_title.get_text(),
                                        "link": find_href
                                        # tags
                                    }
                                )

                response.append({
                    query: result
                })
        except Exception as e:
            print(e)
        finally:
            self.driver.close()
            self.driver.quit()
        return response
