
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
from zhulong.util.etl import gg_meta,gg_html


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)





def f1(driver, num):
    print(num)
    url = driver.current_url


    locator = (By.XPATH, "//div[@style='min-height: 900px; width: 938px']/table/tbody/tr[2]/td/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//a[@class='one']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = int(str)
    except:
        cnum = 1


    if num != int(cnum):
        driver.execute_script('pagination({0});return false;'.format(num))

        try:
            locator = (By.XPATH, "//div[@style='min-height: 900px; width: 938px']/table/tbody/tr[2]/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@style='min-height: 900px; width: 938px']/table/tbody/tr[2]/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", style="min-height: 900px; width: 938px")

    trs = table.find_all("tr")
    data = []
    for tr in trs[1:]:
        a = tr.find('a')
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()

        try:
            link = a["href"]
        except:
            link = ""

        td = tr.find_all("td", style="text-align: center;")[1].text.strip()

        link = "http://www.nmgggzyjy.gov.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)
        print(tmp)
        d = f3(driver, link)
        print(d)



    df = pd.DataFrame(data)
    df['info'] = None
    return df




def f2(driver):
    url = driver.current_url


    locator = (By.XPATH, "//div[@style='min-height: 900px; width: 938px']/table/tbody/tr[2]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='mmggxlh']/a[7]")
        num_total = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    except:
        num_total = 1

    driver.quit()
    return int(num_total)




def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "location clearfloat")
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

    div = soup.find('div', class_="content")
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

def work(conp):
    gg_meta(conp,data=data,diqu="内蒙古自治区省级")

    gg_html(conp,f=f3)

if __name__ == '__main__':
    # conp=["postgres","since2015","192.168.3.171","neimenggu","neimenggu"]
    #
    # work(conp=conp)
    #
    driver=webdriver.Chrome()
    url = "http://www.nmgggzyjy.gov.cn/jyxx/jsgcZbgg"
    driver.get(url)
    df = f2(driver)
    print(df)
    driver = webdriver.Chrome()
    url = "http://www.nmgggzyjy.gov.cn/jyxx/jsgcZbgg"
    driver.get(url)
    for i in range(1, 7):
        df=f1(driver, i)
        print(df)
