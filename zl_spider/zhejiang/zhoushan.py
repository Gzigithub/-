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


_name_="zhoushan"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver, num):

    locator = (By.XPATH, "(//a[@class='WebList_sub'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//td[@class='huifont']")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]
    # print(cnum)
    url = driver.current_url

    if "?Paging" not in url:
        url = url + "?Paging=1"
        driver.get(url)
        cnum = 1

    if num != int(cnum):
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "(//a[@class='WebList_sub'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//a[@class='WebList_sub'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("table", width='98%')

    tbody = table.find("tbody")

    trs = tbody.find_all("tr", height="30")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            link = ''
        tds = tr.find("td", width="80").text
        td = re.findall(r'\[(.*)\]', tds)[0]
        tmp = [a["title"].strip(), td.strip(), "http://www.zsztb.gov.cn" + link.strip()]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, "(//a[@class='WebList_sub'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, '//td[@class="huifont"]')
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "tab")

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

    div = soup.find('td', id='TDContent')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010008/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_biangen_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010009/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjiegou_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010017/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010010/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010011/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010015/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjiegou_weiruwei_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010012/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_liubiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/gcjs/010013/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhaobiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/xzjd/037001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhongbiaohx_gg",
     "http://www.zsztb.gov.cn/zsztbweb/xzjd/037002/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qita_zhaobiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/qtjy/039001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://www.zsztb.gov.cn/zsztbweb/qtjy/039002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_jizhong_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_fensan_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_jinjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_xunjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_jizhong_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011002/011002001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_fensan_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011002/011002002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_jinjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011002/011002003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_xunjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011002/011002004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011003/011003001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_danyilaiyuan_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011003/011003002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_jieguo_jizhong_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011004/011004001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jieguo_fensan_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011004/011004002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_jinjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011004/011004003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_xunjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011004/011004004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jizhong_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011005/011005003/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_fensan_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011005/011005004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jinjia_gg",
     "http://www.zsztb.gov.cn/zsztbweb/zfcg/011005/011005001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]



def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省舟山市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","zhoushan"])


    # driver=webdriver.Chrome()
    # url="http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001004/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver=webdriver.Chrome()
    # url="http://www.zsztb.gov.cn/zsztbweb/zfcg/011001/011001004/"
    # driver.get(url)
    # for i in range(4, 5):
    #     df=f1(driver, i)
    #     print(df)
