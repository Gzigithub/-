from os.path import dirname, join

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
from zhulong.util.etl import add_info, est_meta, est_html, est_tbs, gg_existed

_name_="zhangzhou"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)




num_list = []
title_list = []
j=0


def f1(driver, num):
    url = driver.current_url
    if ("/Front/gcxx/002004/" in url):
        if "info" in url:
            url = url.rsplit('/', maxsplit=1)[0]
            driver.get(url)
        num = f1_click(driver, num, j)
        url = driver.current_url

    # 判断是否是第一次爬取，如果是增量更新,只获取前5页
    if num > CDC_NUM:
        return

    locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = int(str)
    except:
        cnum = 1

    if num != int(cnum):
        if "?Paging" not in url:
            s = "?Paging=%d" % (num) if num > 1 else "?Paging=1"
            url = url + s
        elif num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a[not(contains(string(), '{}'))]".format(val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a[not(contains(string(), '{}'))]".format(val))
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("table", width='99%')

    trs = table.find_all("tr", height="22")
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

        td = tr.find("td", width="80").text.strip()

        link = "http://www.zzgcjyzx.com"+link

        tmp = [title, td, link]
        data.append(tmp)
        # print(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    url = driver.current_url

    if ("/Front/gcxx/002004/" in url):
        global j
        j = 0
        j = int(re.findall(r'info=(\d+)', url)[0])
        url = url.rsplit('/', maxsplit=1)[0]
        # print(url)
        driver.get(url)
        num = f2_num(driver, j)
        driver.quit()
        return num

    locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        driver.find_element_by_xpath('(//img[@align="Baseline"])[last()]').click()
        try:
            locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
            WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator))
        except:
            while True:
                # print("1111")
                driver.find_element_by_xpath('(//img[@align="Baseline"])[2]').click()
                try:
                    # time.sleep(5)
                    locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
                    val = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text
                    if val:
                        locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
                        str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
                        break
                except:
                    locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
                    str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
                    num = int(str_1)
                    if num == 0:
                        break

        locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
        str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(str_1)
        if num == 0:
            num = 1
    except:
        html_data = driver.page_source
        if "本栏目暂时没有内容" in html_data:
            num = 1
        else:
            num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "infodetd")
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

    div = soup.find('table', id="tblInfo")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


def f2_num(driver, j):
    global num_list,title_list
    num_list = []
    title_list = []
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    uls = soup.find_all('font', class_='MoreinfoColor')
    total = len(uls)
    cnum = 0
    list_1 = []
    locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1]")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    # print(str)
    for i in range(1, int(total) + 1):
        locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[{}]".format(i))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        title_list.append(val)
        time.sleep(1)
        locator = (By.XPATH, "(//font[@class='MoreinfoColor'])[{}]".format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1][not(contains(string(), '{}'))]".format(str))
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
        time.sleep(1)
        locator = (By.XPATH, "(//font[@class='MoreinfoColor'])[{}]".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        try:
            driver.find_element_by_xpath('(//img[@align="Baseline"])[last()]').click()
            try:
                locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
                WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator))
            except:
                while True:
                    # print("1111")
                    driver.find_element_by_xpath('(//img[@align="Baseline"])[2]').click()
                    try:
                        # time.sleep(5)
                        locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
                        val = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text
                        if val:
                            locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
                            str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
                            break
                    except:
                        locator = (By.XPATH, "//td[@valign='bottom']/font[2]/b")
                        str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
                        num = int(str_1)
                        if num == 0:
                            break

            locator = (By.XPATH, "//td[@valign='bottom']/font[3]/b")
            str_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            num = int(str_1)
            if num == 0:
                num = 1
        except:
            html_data = driver.page_source
            if "本栏目暂时没有内容" in html_data:
                num = 1
            else:
                num = 1
        cnum += num
        list_1.append(num)
        try:
            driver.find_element_by_xpath("(//font[@class='currentpostionfont'])[4]").click()
        except:
            driver.get('http://www.zzgcjyzx.com/Front/gcxx/002004/')

    for i in range(1, len(list_1) + 1):
        b = sum(list_1[:i])
        num_list.append(b)


    return int(cnum)



def f1_click(driver, num, j):
    list_num = int(len(num_list))
    for i in range(1, list_num+1):
        if i == 1:
            if num <= num_list[i-1]:
                num = num
                f1_data(driver, i, j)
                return num
        else:
            if num_list[i-2] < num <= num_list[i-1]:
                num = num - num_list[i-2]
                f1_data(driver, i, j)
                return num

def f1_data(driver, i, j):
    url = driver.current_url
    try:
        locator = (By.XPATH, "//td[@valign='bottom']/font[1]/b")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val = title_list[i-1]
        locator = (By.XPATH, "(//font[@class='currentpostionfont'])[5]")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if val != str:
            url = url.rsplit('/', maxsplit=3)[0]
            driver.get(url)
            locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1]")
            tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

            locator = (By.XPATH, "(//font[@class='MoreinfoColor'])[{}]".format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1][not(contains(string(), '{}'))]".format(tar))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            locator = (By.XPATH, "(//font[@class='MoreinfoColor'])[{}]".format(j))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            time.sleep(1)
            return
        else:
            return
    except:
        locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1]")
        tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        driver.find_element_by_xpath("(//font[@class='MoreinfoColor'])[{}]".format(i)).click()
        locator = (By.XPATH, "(//td[@class='MoreinfoColor'])[1][not(contains(string(), '{}'))]".format(tar))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "(//font[@class='MoreinfoColor'])[{}]".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, "//table[@width='99%']/tbody/tr[1]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        time.sleep(1)
        return


data = [

    ["gcjs_zhaobiao_shigong_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002001/002001001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_jianli_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002001/002001002/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_sheji_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002001/002001003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_qita_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002001/002001005/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002002/002002001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002002/002002006/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xianzhijia_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002002/002002002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_xianqu_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002004/info=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xianzhijia_xianqu_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002004/info=3",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_xianqu_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002004/info=4",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_zhongbiao_xianqu_gg",
     "http://www.zzgcjyzx.com/Front/gcxx/002004/info=6",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]




def get_profile():
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'r') as f:
        p = f.read()

    return p


def get_conp(txt):
    x = get_profile() + ',' + txt
    arr = x.split(',')
    return arr


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 100000


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省漳州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","zhangzhou"])

    # driver=webdriver.Chrome()
    # url = "http://www.zzgcjyzx.com/Front/gcxx/002001/002001001/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "http://www.zzgcjyzx.com/Front/gcxx/002001/002001001/"
    # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)