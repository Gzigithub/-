
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


_name_="pinghu"





def f1(driver, num):

    locator = (By.XPATH, "//div[@class='bg3 FloatL']/ul/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//div[@class='page-bg FloatR']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1

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
            locator = (By.XPATH, "//div[@class='bg3 FloatL']/ul/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='bg3 FloatL']/ul/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_='bg3 FloatL')

    trs = table.find_all("li")
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

        link = "http://ztb.pinghu.gov.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//div[@class='bg3 FloatL']/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='page-bg FloatR']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(re.findall(r'/(\d+)', str)[0])
    except:
        num = 1
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "Nav")

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

    div = soup.find('div', class_="Content-Main FloatL Black")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/gcjszbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://ztb.pinghu.gov.cn/phcms/gcjszbgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/jsgczbjggs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://ztb.pinghu.gov.cn/phcms/jsgckbjl/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhaobiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://ztb.pinghu.gov.cn/phcms/zfcgzqyj/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://ztb.pinghu.gov.cn/phcms/zfcgbcgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/zfcgzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhaobiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/zbgg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/zbgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_gg",
     "http://ztb.pinghu.gov.cn/phcms/xzzbxx/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://ztb.pinghu.gov.cn/phcms/zjdzbxx/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省平湖市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","pinghu"])



    # driver=webdriver.Chrome()
    # url="http://ztb.pinghu.gov.cn/phcms/jsgc/index.htm"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)