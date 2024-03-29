
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


_name_="wenling"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)






def f1(driver, num):
    url = driver.current_url
    locator = (By.XPATH, "//*[@id='4482116']/div/div/table/tbody/tr[1]/td[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//span[@class='default_pgEndRecord']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(int(str) / 15)
    except:
        cnum = 1

    if num != int(cnum):
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).clear()
        locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
        try:
            locator = (By.XPATH, "//*[@id='4482116']/div/div/table/tbody/tr[1]/td[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//*[@id='4482116']/div/div/table/tbody/tr[1]/td[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_="default_pgContainer")

    trs = table.find_all("tr")
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
            link = ''
        td = tr.find_all("td")[1].text.strip()


        link = "http://new.wl.gov.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    locator = (By.XPATH, "//*[@id='4482116']/div/div/table/tbody/tr[1]/td[1]/a")
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
    locator = (By.CLASS_NAME, "top")
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

    div = soup.find('table', id="c")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://new.wl.gov.cn/col/col1456441/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://new.wl.gov.cn/col/col1456442/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://new.wl.gov.cn/col/col1456444/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://new.wl.gov.cn/col/col1456445/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_jizhong_gg",
     "http://new.wl.gov.cn/col/col1456446/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jizhong_gg",
     "http://new.wl.gov.cn/col/col1456447/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangenyucai_jizhong_gg",
     "http://new.wl.gov.cn/col/col1456448/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_jizhong_gg",
     "http://new.wl.gov.cn/col/col1456450/index.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_fensan_gg",
     "http://new.wl.gov.cn/col/col1456451/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_fensan_gg",
     "http://new.wl.gov.cn/col/col1456452/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_buchong_fensan_gg",
     "http://new.wl.gov.cn/col/col1456452/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://new.wl.gov.cn/col/col1456462/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://new.wl.gov.cn/col/col1456463/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_zhaobiao_gg",
     "http://new.wl.gov.cn/col/col1456464/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://new.wl.gov.cn/col/col1456465/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    # est_meta(conp,data=data,diqu="浙江省温岭市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","wenling"])


    # work(conp=conp)
    # #
    # driver=webdriver.Chrome()
    # url="http://new.wl.gov.cn/col/col1456441/index.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
