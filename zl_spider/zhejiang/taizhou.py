
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


_name_="taizhou"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1
    # print(cnum)
    url = driver.current_url

    if num != int(cnum):
        if "index.htm" in url:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index", s, url)
        elif num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_='Right-Border floatL')

    trs = table.find_all("dt")
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
        td = tr.find("span").text.strip()
        span = re.findall(r'\[(.*)\]', td)[0]

        if "http://www.jhztb.gov.cn/platform/project/notice" in url:
            link = "http://www.jhztb.gov.cn/platform/project/notice/" + link.strip()
        else:
            link = "http://www.tzztb.com" + link.strip()

        tmp = [title, span, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/(\d+)', str)[0]
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
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

    div = soup.find('div', class_='content-Border floatL')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.tzztb.com/tzcms/gcjyzhaobgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zishenjieguo_gg",
     "http://www.tzztb.com/tzcms/gcjyysgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.tzztb.com/tzcms/gcjyzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.tzztb.com/tzcms/gcjyzbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],



    ["zfcg_zhaobiao_gg",
     "http://www.tzztb.com/tzcms/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://www.tzztb.com/tzcms/zfcgggyg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.tzztb.com/tzcms/zfcgzbhxgs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://www.tzztb.com/tzcms/zfcgggwjhxq/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],



    ["gcjs_xiaoer_zhaobiao_gg",
     "http://www.tzztb.com/tzcms/xegccrgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_zhongbiao_gg",
     "http://www.tzztb.com/tzcms/xegccjgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],



    ["qsydw_zhaobiao_gg",
     "http://www.tzztb.com/tzcms/fscggg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_zhongbiao_gg",
     "http://www.tzztb.com/tzcms/fszbgg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省台州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","taizhou"])



    # driver=webdriver.Chrome()
    # url="http://www.tzztb.com/tzcms/fszbgg/index.htm"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)