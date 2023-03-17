from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import multiprocessing
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
chrome_options.add_argument('headless')
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument("disable-gpu")

def get_id():
    url = 'https://github.com/sammy310/Danawa-Crawler/raw/master/crawl_data/Laptop.csv'
    df = pd.read_csv(url, usecols=['Id'])
    id_list = df['Id'].to_list()
    # print(id_list)
    return id_list

def crawling(id_list):
    check_url = f"https://prod.danawa.com/info/?pcode={id_list}&cate=112758"
    url = check_url
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)  # 페이지 로딩
    web = BeautifulSoup(driver.page_source, 'html.parser')  # 로딩된 페이지의 소스코드를 다시 가져옴
    desc = web.find('meta', property="og:description")['content']
    name = web.find('title')
    price = web.find('span','lwst_prc')
    print(name.text, price.text)
    try:
        return name.text, desc, price.text
    except:
        return name.text, desc, None

if __name__ == '__main__':
    start = time.time()
    id_list = get_id()
    id_list = id_list[:100]
    names = []
    descriptions = []
    prices = []

    # 병렬화 2 or 3
    with multiprocessing.Pool(2) as p: 
        result = p.map(crawling, id_list)
    for i in result:
        names.append(i[0])
        descriptions.append(i[1])
        prices.append(i[2])
    # 기본
    # for id in id_list:
    #     name, desc, price = crawling(id)
    #     names.append(name)
    #     descriptions.append(desc)
    #     prices.append(price)
    dedf = pd.DataFrame({'name':names, 'price':prices, 'desc':descriptions})
    dedf.to_csv("laptop.csv", index=False)
    end = time.time()
    print(end - start)