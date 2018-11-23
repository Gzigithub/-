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


_name_="quzhou"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

num_list = []

def f1(driver, num):

    url = driver.current_url

    locator = (By.XPATH, "(//ul[@class='ewb-news-items']/li/a)[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//li[@class='ewb-page-li ewb-page-noborder ewb-page-num']/span")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1

    # print(cnum)
    if num != int(cnum):
        if num == 1:
            url = re.sub("/[0-9]*\.html", "/1.html", url)
        else:
            s = "/%d.html" % (num) if num > 1 else "/1.html"
            url = re.sub("/[0-9]*\.html", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//ul[@class='ewb-news-items']/li/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//ul[@class='ewb-news-items']/li/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_='ewb-news-items')

    trs = table.find_all("li")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            link = ''
        td = tr.find("span", class_="ewb-news-date").text
        tmp = [a["title"].strip(), td.strip(), "http://www.qzggzy.com" + link.strip()]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):

    locator = (By.XPATH, "(//ul[@class='ewb-news-items']/li/a)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//li[@class='ewb-page-li ewb-page-noborder ewb-page-num']/span")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/(\d+)', str)[0]
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "container")

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

    div = soup.find('div', class_='ewb-details-info')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.qzggzy.com/jyxx/002001/002001001/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_biangen_gg",
     "http://www.qzggzy.com/jyxx/002001/002001002/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.qzggzy.com/jyxx/002001/002001004/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.qzggzy.com/jyxx/002001/002001006/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://www.qzggzy.com/jyxx/002002/002002001/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_gg",
     "http://www.qzggzy.com/jyxx/002002/002002002/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_danyiyucai_gg",
     "http://www.qzggzy.com/jyxx/002002/002002004/1.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_qita_gg",
     "http://www.qzggzy.com/jyxx/002002/002002005/1.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["qsydw_zhaobiao_gg",
     "http://www.qzggzy.com/jyxx/002004/002004001/002004001001/1.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_biangen_gg",
     "http://www.qzggzy.com/jyxx/002004/002004002/002004002001/1.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://www.qzggzy.com/jyxx/002004/002004004/002004004001/1.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiaohx_gg",
     "http://www.qzggzy.com/jyxx/002004/002004003/002004003001/1.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    # est_meta(conp,data=data,diqu="浙江省衢州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","quzhou"])


    # driver=webdriver.Chrome()
    # url="http://www.qzggzy.com/jyxx/002002/002002001/1.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "http://www.qzggzy.com/jyxx/002002/002002001/1.html"
    # driver.get(url)
    # for i in range(245, 249):
    #     df=f1(driver, i)
    #     print(df)
