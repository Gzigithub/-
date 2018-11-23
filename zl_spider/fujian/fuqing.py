
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


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

num_total = 0

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="fuqing"


def f1(driver, num):
    url = driver.current_url
    locator = (By.XPATH, "//ul[@id='list']/li[2]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, '//span[@class="cPageNum"]')
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(str)
    except:
        cnum = 1

    if num != int(cnum):
        driver.execute_script("pageNav.go({0},{1},'pageNav');".format(num, num_total))

        try:
            locator = (By.XPATH, "//ul[@id='list']/li[2]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@id='list']/li[2]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", id="list")

    trs = table.find_all("li")
    data = []
    for tr in trs[1:]:
        a = tr.find('a')
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()

        try:
            link = a["href"]
        except:
            link = ""

        td = tr.find("span").text.strip()

        link = "http://www.fqztb.com"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)



    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    global num_total
    num_total = 0
    url = driver.current_url
    locator = (By.XPATH, "//ul[@id='list']/li[2]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@id='pageNav']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num_total = re.findall(r'共 (\d+) 页', str)[0]
    except:
        num_total = 1

    driver.quit()
    return int(num_total)




def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "main")
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

    div = soup.find('div', class_="wrap")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.fqztb.com/Home/tenderList?index=3&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_qita_gg",
     "http://www.fqztb.com/Home/TenderList_result?index=4&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE",
     ["name", "ggstart_time", "href", "info"],f1,f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省福清市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","fuqing"])
    #
    # driver=webdriver.Chrome()
    # url = "http://www.fqztb.com/Home/tenderList?index=3&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "http://www.fqztb.com/Home/tenderList?index=3&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE"
    # driver.get(url)
    # for i in range(3, 7):
    #     df=f1(driver, i)
    #     print(df)
