
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


_name_="fuzhou"





def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='article-list2']/li[1]/div/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//ul[@class='pages-list']/li[1]/a")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1
    url = driver.current_url

    if num != int(cnum):
        if "index.jhtml" in url:
            s = "index_%d.jhtml" % (num) if num > 1 else "index_1.jhtml"
            url = re.sub("index.jhtml", s, url)
        elif num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "//ul[@class='article-list2']/li[1]/div/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@class='article-list2']/li[1]/div/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_="article-list2")

    trs = table.find_all("li")
    data = []
    for tr in trs:
        a = tr.find('a')

        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()

        try:
            link = a["href"]
        except:
            link = ''

        td = tr.find("div", class_='list-times').text.strip()

        link = "http://fzsggzyjyfwzx.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//ul[@class='article-list2']/li[1]/div/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//ul[@class='pages-list']/li[1]/a")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = re.findall(r'/(\d+)', str)[0]
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "content")
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

    div = soup.find('div', id="content")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_yuzhaobiao_gg",
     "http://fzsggzyjyfwzx.cn/jyxxzbxm/index.jhtml",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_gg",
     "http://fzsggzyjyfwzx.cn/jyxxzbgg/index.jhtml",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://fzsggzyjyfwzx.cn/jyxxgcbc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zishenjieguo_gg",
     "http://fzsggzyjyfwzx.cn/jyxxkbjl/index.jhtml",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://fzsggzyjyfwzx.cn/jyxxzsjg/index.jhtml",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://fzsggzyjyfwzx.cn/jyxxzbgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://fzsggzyjyfwzx.cn/jyxxcggg/index.jhtml",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://fzsggzyjyfwzx.cn/jyxxgzsx/index.jhtml",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://fzsggzyjyfwzx.cn/jyxxcjgg/index.jhtml",
    ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zishenjieguo_gg",
     "http://fzsggzyjyfwzx.cn/jyxxcgxq/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省福州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","fuzhou"])


    #
    # driver=webdriver.Chrome()
    # url = "http://fzsggzyjyfwzx.cn/jyxxcggg/index.jhtml"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
