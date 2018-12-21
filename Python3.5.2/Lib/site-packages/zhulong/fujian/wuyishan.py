
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


_name_="wuyishan"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)





def f1(driver, num):
    url = driver.current_url

    locator = (By.XPATH, "//div[@class='ny_list']/ul/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//div[@class='ny_yqt']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1


    if num != int(cnum):
        if num == 1:
            url = re.sub("currentPage=[0-9]*", "currentPage=1", url)
        else:
            s = "currentPage=%d" % (num) if num > 1 else "currentPage=1"
            url = re.sub("currentPage=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "//div[@class='ny_list']/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='ny_list']/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_="ny_list")

    trs = table.find_all("li")
    data = []
    for tr in trs:
        a = tr.find('a')
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()

        try:
            link = a["href"]
        except:
            link = ""

        span = tr.find("span", class_="bidspan").text.strip()
        td = re.findall(r"(\d+-\d+-\d+)", span)[0]


        link = "http://www.wysggzy.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)
        print(tmp)



    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    url = driver.current_url


    locator = (By.XPATH, "//div[@class='ny_list']/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='ny_yqt']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num_total = re.findall(r'/(\d+)', str)[0]
    except:
        num_total = 1

    driver.quit()
    return int(num_total)




def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "main")
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

    div = soup.find('div', class_="wrap")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    # ["gcjs_zhaobiao_gg",
    #  "http://www.fqztb.com/Home/tenderList?index=3&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE",
    #  ["name", "ggstart_time", "href", "info"],f1,f2],
    #
    # ["gcjs_zhongbiao_qita_gg",
    #  "http://www.fqztb.com/Home/TenderList_result?index=4&type=%E5%B7%A5%E7%A8%8B%E5%BB%BA%E8%AE%BE",
    #  ["name", "ggstart_time", "href", "info"],f1,f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省武夷山市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    # work(conp=["postgres","since2015","192.168.3.171","fujian","wuyishan"])

    #
    driver=webdriver.Chrome()
    url = "http://www.wysggzy.cn/wysebid/website/infolist.jsp?clsid=BID_BULLETIN&tid=F&bultype=&pid=1&keyword=&bgdate=&eddate=&currentPage=1&menuid=1&projStatus=#"
    driver.get(url)
    df = f2(driver)
    print(df)
    driver = webdriver.Chrome()
    url = "http://www.wysggzy.cn/wysebid/website/infolist.jsp?clsid=BID_BULLETIN&tid=F&bultype=&pid=1&keyword=&bgdate=&eddate=&currentPage=1&menuid=1&projStatus=#"
    driver.get(url)
    for i in range(3, 7):
        df=f1(driver, i)
        print(df)
