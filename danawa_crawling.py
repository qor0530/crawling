from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from multiprocessing import Pool 

import pandas as pd

descriptions = []
names = []
url = 'https://github.com/sammy310/Danawa-Crawler/raw/master/crawl_data/Laptop.csv'
df = pd.read_csv(url, usecols=['Id'])

dic_list = df['Id'].to_list()
for id in dic_list[:5]:
    check_url = f"https://prod.danawa.com/info/?pcode={id}&cate=112758"
    url = check_url
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)  # 페이지 로딩
    web = BeautifulSoup(driver.page_source, 'html.parser')  # 로딩된 페이지의 소스코드를 다시 가져옴
    desc = web.find('meta', property="og:description")['content']
    name = web.find('title')
    descriptions.append(desc[32:])
    names.append(name.text)
    print(desc, name.text)
dedf = pd.DataFrame({'name':names, 'desc':descriptions})

dedf.to_csv("descriptions.csv", index=False)