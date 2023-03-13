from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
# 나중에 빠르게 할때 병렬화 공부 
# from multiprocessing import Pool 
import pandas as pd

url = 'https://github.com/sammy310/Danawa-Crawler/raw/master/crawl_data/Laptop.csv'
df = pd.read_csv(url, usecols=['Id'])

print(df)
dic_list = df['Id'].to_list()
print(dic_list)
for id in dic_list:
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
    print(desc[32:]) # 좀 더 스마트한 방법으로 ... ㅎ