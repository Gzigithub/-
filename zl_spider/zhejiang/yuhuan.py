
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


_name_="yuhuan"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)





def f1(driver, num):
    locator = (By.XPATH, "(//span[@class='f18'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//li[@class='active']/a")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = int(str)
    except:
        cnum = 1

    url = driver.current_url
    if num != int(cnum):
        if "pageIndex" not in url:
            s = "?pageIndex=%d" % (num) if num > 1 else "?pageIndex=1"
            url = url + s
        elif num == 1:
            url = re.sub("pageIndex=[0-9]*", "pageIndex=1", url)
        else:
            s = "pageIndex=%d" % (num) if num > 1 else "pageIndex=1"
            url = re.sub("pageIndex=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//span[@class='f18'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//span[@class='f18'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_="filter-content")

    ul = table.find("ul")

    trs = ul.find_all("li")
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
        td = tr.find("span", class_="time").text.strip()
        span = re.findall(r'(\d+/\d+/\d+)', td)[0]

        links = "https://www.yhjyzx.com"+link.strip()

        tmp = [title, span, links]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):

    locator = (By.XPATH, "(//span[@class='f18'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//*[@id='bootstrappager']/li[last()]/a")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).get_attribute('href')
        num = re.findall(r'pageIndex=(\d+)', str)[0]
    except:
        num = 1
    driver.quit()
    return int(num)



def f3(driver, url):
    if "DetailTransactionInfo" in url:
        driver.get(url)
        locator = (By.CLASS_NAME, "pre-header")
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

        div = soup.find('div', class_="inner-main-content")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    driver.get(url)
    locator = (By.CLASS_NAME, "pre-header")
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

    div = soup.find('div', class_="details-content")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_yuzhaobiao_gg",
     "https://www.yhjyzx.com/TransactionInfo/jsgc/xmdjxx",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/jsgc/zbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_biangen_gg",
     "https://www.yhjyzx.com/BidNotice/jsgc/bggg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zishenjieguo_gg",
     "https://www.yhjyzx.com/BidNotice/jsgc/kbqk",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "https://www.yhjyzx.com/BidNotice/jsgc/zbhxrgs",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "https://www.yhjyzx.com/BidNotice/jsgc/zbjggg",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "https://www.yhjyzx.com/TransactionInfo/jsgc/zbtzs",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/zqyj",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/cggg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/bggg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zishenjieguo_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/kbjggg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiaohx_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/cjhxrgs",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/zbjggg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_liubiao_gg",
     "https://www.yhjyzx.com/BidNotice/zfcg/fbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/gyqywzcg/zbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_biangen_gg",
     "https://www.yhjyzx.com/BidNotice/gyqywzcg/gzgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "https://www.yhjyzx.com/BidNotice/gyqywzcg/cjgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_bumen_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/bmzb/zbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_bumen_biangen_gg",
     "https://www.yhjyzx.com/BidNotice/bmzb/gzgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_bumen_zhongbiao_gg",
     "https://www.yhjyzx.com/BidNotice/bmzb/cjgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/qtggzyjy/hysyq/zbgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "https://www.yhjyzx.com/BidNotice/qtggzyjy/hysyq/cjgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_zhaobiao_gg",
     "https://www.yhjyzx.com/BidNotice/Qtxm/xxgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_biangen_gg",
     "https://www.yhjyzx.com/BidNotice/Qtxm/gzgg",
     ["name", "ggstart_time", "href", "info"], f1, f2],
]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省玉环市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","yuhuan"])

    # #
    # driver=webdriver.Chrome()
    # url="https://www.yhjyzx.com/TransactionInfo/jsgc/zbtzs"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
