
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


from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="cixi"


def f1(driver, num):

    locator = (By.XPATH, "//div[@class='default_pgContainer']/table[2]")
    val = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//span[@class='default_pgEndRecord']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(int(str)/15)
    except:
        cnum = 1


    if num != int(cnum):
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).clear()
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
        try:
            locator = (By.XPATH, "//div[@class='default_pgContainer']/table[2][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='default_pgContainer']/table[2][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_='default_pgContainer')

    trs = table.find_all("table")
    data = []
    for tr in trs[1:]:
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

        link = link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    locator = (By.XPATH, "//div[@class='default_pgContainer']/table[2]")
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

    locator = (By.CLASS_NAME, "menu")

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))

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

    div = soup.find('div', style="text-align:center;")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://ztb.cixi.gov.cn/col/col13403/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_biangen_gg",
     "http://ztb.cixi.gov.cn/col/col77304/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://ggzy.cixi.gov.cn/col/col13404/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhaobiao_gg",
     "http://ggzy.cixi.gov.cn/col/col13405/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhongbiao_gg",
     "http://ggzy.cixi.gov.cn/col/col13406/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg",
     "http://ggzy.cixi.gov.cn/col/col78663/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://ggzy.cixi.gov.cn/col/col78664/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["qsydw_zhaobiao_gg",
     "http://ggzy.cixi.gov.cn/col/col16429/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://ggzy.cixi.gov.cn/col/col16430/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_zhaobiao_gg",
     "http://ggzy.cixi.gov.cn/col/col16431/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://ggzy.cixi.gov.cn/col/col16432/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省慈溪市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","cixi"])


    # driver=webdriver.Chrome()
    # url="http://ggzy.cixi.gov.cn/col/col78664/index.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
