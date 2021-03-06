
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


_name_="fujian"





def f1(driver, num):
    locator = (By.XPATH, "(//span[@class='article-list-text'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//ul[@class='pagination']/li[@class='active']/a")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(str)
    except:
        cnum = 1
    url = driver.current_url

    if num != int(cnum):
        if "page" not in url:
            s = "?page=%d" % (num) if num > 1 else "?page=1"
            url = url + s
        elif num == 1:
            url = re.sub("page=[0-9]*", "page=1", url)
        else:
            s = "page=%d" % (num) if num > 1 else "page=1"
            url = re.sub("page=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "(//span[@class='article-list-text'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//span[@class='article-list-text'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_="article-list-template")

    trs = table.find_all("a")
    data = []
    for tr in trs:

        try:
            prj_nums = tr.find("span", class_='article-list-number')
            prj_num = prj_nums.find("span").text.strip()
        except:
            prj_num = ""

        try:
            title = tr["title"].strip()
        except:
            title = tr.find("span", class_='article-list-text').text.strip()

        try:
            link = tr["href"]
        except:
            continue

        td = tr.find("span", class_='article-list-date').text.strip()

        link = "http://www.fjggzyjy.cn"+link.strip()

        tmp = [prj_num, title, td, link]
        data.append(tmp)
        # print(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "(//span[@class='article-list-text'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//a[@class='end']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = int(str)
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "layout-head")
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

    div = soup.find('div', class_="layout-article")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_fangjian_zhaobiao_gg",
     "http://www.fjggzyjy.cn/news/category/46/",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_fangjian_zhongbiaohx_gg",
     "http://www.fjggzyjy.cn/news/category/49/",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_fangjian_zhongbiao_gg",
     "http://www.fjggzyjy.cn/news/category/50/",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_jiaotong_zhaobiao_gg",
     "http://www.fjggzyjy.cn/news/category/52/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_jiaotong_gg",
     "http://www.fjggzyjy.cn/news/category/54/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_jiaotong_zhongbiaohx_gg",
     "http://www.fjggzyjy.cn/news/category/55/",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_jiaotong_zhongbiao_gg",
     "http://www.fjggzyjy.cn/news/category/56/",
     ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://www.fjggzyjy.cn/news/category/10/",
    ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://www.fjggzyjy.cn/news/category/11/",
    ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jieguo_gg",
     "http://www.fjggzyjy.cn/news/category/12/",
    ["prj_num", "name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_jingjia_zhaobiao_gg",
     "http://www.fjggzyjy.cn/news/category/14/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jingjia_gg",
     "http://www.fjggzyjy.cn/news/category/78/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jingjia_jieguo_gg",
     "http://www.fjggzyjy.cn/news/category/16/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_qita_gg",
     "http://www.fjggzyjy.cn/news/category/17/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://www.fjggzyjy.cn/news/category/58/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_gg",
     "http://www.fjggzyjy.cn/news/category/60/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiaohx_gg",
     "http://www.fjggzyjy.cn/news/category/61/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://www.fjggzyjy.cn/news/category/62/",
     ["prj_num", "name", "ggstart_time", "href", "info"], f1, f2],

]



def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省省级",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","fujian"])


    # driver=webdriver.Chrome()
    # url = "http://www.fjggzyjy.cn/news/category/202/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
