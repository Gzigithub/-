
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


_name_="tongxiang"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    locator = (By.XPATH, "(//a[@class='ewb-list-name-1'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1

    url = driver.current_url

    if num != int(cnum):
        driver.execute_script("ShowNewPage('./moreinfolist.aspx?title=&startdate=&enddate=&categoryNum=007001&Paging={}');".format(num))
        try:
            locator = (By.XPATH, "(//a[@class='ewb-list-name-1'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//a[@class='ewb-list-name-1'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_='ewb-dynamic-list')

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
        td = tr.find("span", class_='ewb-list-date-1').text.strip()

        link = "http://ztb.txggfw.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "(//a[@class='ewb-list-name-1'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(re.findall(r'/(\d+)', str)[0])
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "ewb-top")

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

    div = soup.find('div', class_="article-content")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=007001",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=007003",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=007004",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=007005",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhaobiao_gg",
     "http://ztb.txggfw.cn/web/showinfo/moreinfolist.aspx?categorynum=008001001",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=008001002",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=008001003",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=008001004",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhaobiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=011002001",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=011002002",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhaobiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=011003001",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=011003002",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省桐乡市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","tongxiang"])


    # driver=webdriver.Chrome()
    # url="http://ztb.txggfw.cn/txcms/showinfo/moreinfolist.aspx?categorynum=007001"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
