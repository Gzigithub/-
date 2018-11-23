
import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
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

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="quanzhou"




def f1(driver, num):
    url = driver.current_url
    if ("/project/projectList.do?" in url) or ("/project/otherBidInfo.do?" in url):
        locator = (By.XPATH, "//dl[@id='LatestListPro']/table/tbody/tr[2]/td[2]/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//span[@id='pageIndex']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            cnum = int(str)
        except:
            cnum = 1
        if num != int(cnum):
            s1 = Select(driver.find_element_by_id('skipPage'))
            s1.select_by_value("{}".format(num))
            try:
                locator = (By.XPATH, "//dl[@id='LatestListPro']/table/tbody/tr[2]/td[2]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (By.XPATH, "//dl[@id='LatestListPro']/table/tbody/tr[2]/td[2]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find("dl", id="LatestListPro")
        trs = table.find_all("tr")
        data = []
        for tr in trs[1:]:
            a = tr.find('a')
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"].strip()
            except:
                link = ''
            td = tr.find_all("td", class_="cztab_bt3 cztab_bort cztab_bo")[3].text.strip()
            link = "http://www.qzzb.gov.cn"+link +"&leftIndex=1"
            tmp = [title, td, link]
            data.append(tmp)

        df = pd.DataFrame(data)
        df['info'] = None
        return df

    elif "govProcurement/govMorePage.do?" in url:
        locator = (By.XPATH, "//ul[@id='DetailList']/li[1]/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//span[@id='pageIndex']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            cnum = int(str)
        except:
            cnum = 1
        if num != int(cnum):
            s1 = Select(driver.find_element_by_id('skipPage'))
            s1.select_by_value("{}".format(num))
            try:
                locator = (
                    By.XPATH, "//ul[@id='DetailList']/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (
                    By.XPATH, "//ul[@id='DetailList']/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find("ul", id="DetailList")
        trs = table.find_all("li")
        data = []
        for tr in trs:
            a = tr.find('a')
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"].strip()
            except:
                link = ''
            td = tr.find("span").text.strip()
            link = "http://www.qzzb.gov.cn" + link
            tmp = [title, td, link]
            data.append(tmp)

        df = pd.DataFrame(data)
        df['info'] = None
        return df


    else:
        locator = (By.XPATH, "//dl[@id='LatestListWinBul']/ul/li[1]/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//span[@id='pageIndex']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            cnum = int(str)
        except:
            cnum = 1
        if num != int(cnum):
            s1 = Select(driver.find_element_by_id('skipPage'))
            s1.select_by_value("{}".format(num))
            try:
                locator = (
                By.XPATH, "//dl[@id='LatestListWinBul']/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (
                By.XPATH, "//dl[@id='LatestListWinBul']/ul/li[1]/a[not(contains(string(),'%s'))]" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find("dl", id="LatestListWinBul")
        trs = table.find_all("li")
        data = []
        for tr in trs:
            a = tr.find('a')
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"].strip()
            except:
                link = ''
            td = tr.find("span").text.strip()
            link = "http://www.qzzb.gov.cn" + link
            tmp = [title, td, link]
            data.append(tmp)

        df = pd.DataFrame(data)
        df['info'] = None
        return df


def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//dl[@id='LatestListWinBul']/ul/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@id='totalPage']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = int(str)
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)
    if "/govProcurement/govProcurementDetail.do" in url:
        locator = (By.CLASS_NAME, "warp")
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

        div = soup.find('div', class_="conwz")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    try:
        time.sleep(1)
        al = driver.switch_to_alert()
        al.accept()
        html = driver.page_source
        if "文件存在问题，请联系管理员!" in html:
            return
    except:
        time.sleep(1)
    html = driver.page_source
    if "Internal Server Error" in html:
        return

    time.sleep(1)
    locator = (By.CLASS_NAME, "process")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    time.sleep(1)
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

    time.sleep(3)
    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find('dl', id="ProjectReleDetail")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [

    ["gcjs_zhaobiao_gg",
     "http://www.qzzb.gov.cn/project/projectList.do?centerId=-1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://www.qzzb.gov.cn/project/winBulletinList.do?centerId=-1",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_zhaobiao_gg",
     "http://www.qzzb.gov.cn/govProcurement/govMorePage.do?govProClassId=2&centerId=-1",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://www.qzzb.gov.cn/govProcurement/govMorePage.do?govProClassId=3&centerId=-1",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jieguo_gg",
     "http://www.qzzb.gov.cn/govProcurement/govMorePage.do?govProClassId=4&centerId=-1",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_jieguo_gg",
     "http://www.qzzb.gov.cn/govProcurement/govMorePage.do?govProClassId=5&centerId=-1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg",
     "http://www.qzzb.gov.cn/govProcurement/govMorePage.do?govProClassId=8&centerId=-1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://www.qzzb.gov.cn/project/otherBidInfo.do?centerId=-1",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_gg",
     "http://www.qzzb.gov.cn/project/otherBidWinBulletin.do?centerId=-1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省泉州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","quanzhou"])


    # driver=webdriver.Chrome()
    # url = "http://www.qzzb.gov.cn/project/winBulletinList.do?centerId=-1"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    #
    # for i in range(100, 160):
    #     df=f1(driver, i)
    #     print(df)