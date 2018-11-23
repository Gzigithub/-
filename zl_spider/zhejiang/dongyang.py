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


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="dongyang"


def f1(driver, num):
    locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    url = driver.current_url

    if 'index.htm' in url:
        url = re.sub('index.htm', 'index_1.htm', url)
        driver.get(url)

    locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]
    if num != int(cnum):
        if num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)

        driver.get(url)

        try:
            locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div= soup.find("div", class_='Right-Border floatL')

    trs = div.find_all("dt")
    data = []
    tt = 0
    if "http://www.dyztb.com/zfcg" in url:
        tt = 1

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
        span = tr.find("span").text
        span = re.findall(r'\[(.*)\]', span)[0]

        if tt == 0:
            link = "http://www.dyztb.com" + link.strip()

        tmp = [title, span.strip(), link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    url = driver.current_url
    locator = (By.XPATH, "//div[@class='Right-Border floatL']/dl/dt[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    if "http://www.zjzfcg.gov.cn/" in url:
        driver.get(url)
        locator = (By.CLASS_NAME, "gpoz-line")

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

        div = soup.find('div', class_='gpoz-detail-content')
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif ("http://www.dyztb.com/dybcgg/" in url) or ("http://www.dyztb.com/pbjggs/" in url) or ("http://www.dyztb.com/xzzbgg/" in url):
        driver.get(url)
        locator = (By.CLASS_NAME, "Head")

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

        div = soup.find('div', class_='Main-p floatL')
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    else:
        driver.get(url)
        locator = (By.CLASS_NAME, "Head")

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

        div = soup.find('img', class_='Wzimg')
        # div=div.find_all('div',class_='ewb-article')[0]

        return div



data = [
    ["gcjs_zhaobiao_gg","http://www.dyztb.com/jsgcgcjszbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg", "http://www.dyztb.com/jsgcgcjsdycq/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg", "http://www.dyztb.com/jsgcgcjspbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg", "http://www.dyztb.com/jsgcgcjszbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg", "http://www.dyztb.com/zfcgggyg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg", "http://www.dyztb.com/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_gg", "http://www.dyztb.com/zfcgzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg", "http://www.dyztb.com/zfcgzbhxgs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["qsydw_zhaobiao_gg", "http://www.dyztb.com/xzzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_gg", "http://www.dyztb.com/dybcgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_jieguo_gg", "http://www.dyztb.com/pbjggs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省东阳市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","dongyang"])


    # driver=webdriver.Chrome()
    # url="http://www.dyztb.com/pbjggs/index.htm"
    # driver.get(url)
    # # driver.set_page_load_timeout(2)
    # # driver.set_script_timeout(2)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
