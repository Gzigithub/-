
import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

import json
from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="shengzhou"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    locator = (By.XPATH, "//div[@class='default_pgContainer']/table[1]//a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//span[@class='default_pgEndRecord']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(int(str) / 20)
    except:
        cnum = 1

    if num != int(cnum):
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).clear()
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
        try:
            locator = (By.XPATH, "//div[@class='default_pgContainer']/table[1]//a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='default_pgContainer']/table[1]//a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_="default_pgContainer")

    trs = table.find_all("table")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()
        try:
            link = a["href"]
        except:
            continue
        td = tr.find("td", width="80").text.strip()
        td = re.findall(r'\[(.*)\]', td)[0]

        link = "http://www.szztb.gov.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//div[@class='default_pgContainer']/table[1]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@class='default_pgTotalPage']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = int(str)
    except:
        num = 1
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "STYLE9")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))


    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find('table', width="90%")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.szztb.gov.cn/col/col1940/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.szztb.gov.cn/col/col1941/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://www.szztb.gov.cn/col/col1942/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhaobiao_gg",
     "http://www.szztb.gov.cn/col/col1943/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.szztb.gov.cn/col/col1944/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://www.szztb.gov.cn/col/col1945/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_gg",
     "http://www.szztb.gov.cn/col/col1946/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_zhaobiao_gg",
     "http://www.szztb.gov.cn/col/col1937/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiaohx_gg",
     "http://www.szztb.gov.cn/col/col1938/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://www.szztb.gov.cn/col/col1939/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]

def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省嵊州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","shengzhou"])

    #
    # driver=webdriver.Chrome()
    # url="http://www.szztb.gov.cn/col/col1940/index.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)