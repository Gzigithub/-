
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


_name_="yiwu"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='ewb-nbd-items']/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//span[@id='index']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1

    url = driver.current_url

    if num != int(cnum):
        if ("list3gc.html" in url) or ("list3" in url) or ("list3qt" in url):
            s = "/%d.html" % (num) if num > 1 else "/1.html"
            url = re.sub("/list3gc\.html", s, url)
            url = re.sub("/list3\.html", s, url)
            url = re.sub("/list3qt\.html", s, url)
        elif num == 1:
            url = re.sub("/[0-9]*\.html", "/1.html", url)
        else:
            s = "/%d.html" % (num) if num > 1 else "/1.html"
            url = re.sub("/[0-9]*\.html", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "//ul[@class='ewb-nbd-items']/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@class='ewb-nbd-items']/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_='ewb-nbd-items')

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
        td = tr.find("span", class_="ewb-date r").text.strip()

        link = "http://ywjypt.com"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//ul[@class='ewb-nbd-items']/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@id='index']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(re.findall(r'/(\d+)', str)[0])
    except:
        num = 1
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "ewb-body")

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

    div = soup.find('div', class_="news-article")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [

    ["gcjs_yuzhaobiao_gg",
     "http://ywjypt.com/jyxx/070001/070001015/list3gc.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_gg",
     "http://ywjypt.com/jyxx/070001/070001001/list3gc.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_biangen_gg",
     "http://ywjypt.com/jyxx/070001/070001006/list3gc.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_liubiao_gg",
     "http://ywjypt.com/jyxx/070001/070001007/list3gc.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://ywjypt.com/jyxx/070001/070001009/list3gc.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://ywjypt.com/jyxx/070001/070001004/list3gc.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_dingbiao_gg",
     "http://ywjypt.com/jyxx/070001/070001008/list3gc.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_zhongbiao_gg",
     "http://ywjypt.com/jyxx/070001/070001005/list3gc.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_zhaobiao_gg",
     "http://ywjypt.com/jyxx/070002/070002001/list3.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://ywjypt.com/jyxx/070002/070002004/list3.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://ywjypt.com/jyxx/070002/070002003/list3.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://ywjypt.com/jyxx/070002/070002002/list3.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yanshou_gg",
     "http://ywjypt.com/jyxx/070002/070002008/list3.html",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_yucai_gg",
     "http://ywjypt.com/jyxx/070005/070005003/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://ywjypt.com/jyxx/070005/070005001/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_biangen_gg",
     "http://ywjypt.com/jyxx/070005/070005002/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiaohx_gg",
     "http://ywjypt.com/jyxx/070005/070005006/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_dingbiao_gg",
     "http://ywjypt.com/jyxx/070005/070005010/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://ywjypt.com/jyxx/070005/070005004/list3.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhaobiao_gg",
     "http://ywjypt.com/jyxx/070008/070008001/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_biangen_gg",
     "http://ywjypt.com/jyxx/070008/070008002/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://ywjypt.com/jyxx/070008/070008003/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_yucai_gg",
     "http://ywjypt.com/jyxx/070008/070008007/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_zhaobiao_gg",
     "http://ywjypt.com/jyxx/070008/070008004/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_biangen_gg",
     "http://ywjypt.com/jyxx/070008/070008005/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_xiangzhen_zhongbiao_gg",
     "http://ywjypt.com/jyxx/070008/070008006/list3qt.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省义乌市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","yiwu"])

    # driver=webdriver.Chrome()
    # url="http://ywjypt.com/jyxx/070005/070005006/list3.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
