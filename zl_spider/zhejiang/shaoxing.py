import pandas as pd
import re

from lxml import etree
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


_name_="shaoxing"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver, num):
    url = driver.current_url
    locator = (By.XPATH, "//*[@id='4685909']/div/ul[1]/li/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    if "pageNum" in url:
        cnum = re.findall(r'pageNum=(\d+)', url)[0]
    else:
        cnum = 1

    if num != int(cnum):
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).clear()
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
        locator = (By.XPATH, "//*[@id='4685909']/div/ul[1]/li/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find("div", class_='default_pgContainer')

    trs = div.find_all("ul", class_='ajax-list')
    data = []
    for tr in trs:
        a = tr.find('a')
        title = a.text
        link = "http://ggb.sx.gov.cn" + a['href']
        date = tr.find('span').text.strip()
        date = re.findall(r'\[(.*)\]', date)[0]

        tmp = [title.strip(), date, link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//*[@id='4685909']/div/ul[1]/li/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//span[@class='default_pgTotalPage']")
    num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.ID, "zoom")
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

    div = soup.find('div', id='zoom')
    # div=div.find_all('div',class_='ewb-article')[0]
    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://ggb.sx.gov.cn/col/col1518854/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://ggb.sx.gov.cn/col/col1518855/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://ggb.sx.gov.cn/col/col1518856/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://ggb.sx.gov.cn/col/col1518857/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_yucai_gg",
     "http://ggb.sx.gov.cn/col/col1518859/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://ggb.sx.gov.cn/col/col1518860/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://ggb.sx.gov.cn/col/col1518861/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_liubiao_gg",
     "http://ggb.sx.gov.cn/col/col1518862/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["qsydw_zhaobiao_gg",
     "http://ggb.sx.gov.cn/col/col1518878/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhongbiao_gg",
     "http://ggb.sx.gov.cn/col/col1518879/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_quxian_zhaobiao_gg",
     "http://ggb.sx.gov.cn/col/col1518891/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_quxian_zhongbiaohx_gg",
     "http://ggb.sx.gov.cn/col/col1518892/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_quxian_zhongbiao_gg",
     "http://ggb.sx.gov.cn/col/col1518893/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_quxian_zhaobiao_gg",
     "http://ggb.sx.gov.cn/col/col1518895/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_quxian_yucai_gg",
     "http://ggb.sx.gov.cn/col/col1518894/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_quxian_zhongbiao_gg",
     "http://ggb.sx.gov.cn/col/col1518896/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省绍兴市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","shaoxing"])


    # driver=webdriver.Chrome()
    # url="http://ggb.sx.gov.cn/col/col1518896/index.html"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 16):
    #     df=f1(driver, i)
    #     print(df)
