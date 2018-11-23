from os.path import join, dirname

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

_name_="putian"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)




num_list = []
title_list = []

def f1(driver, num):
    url = driver.current_url
    if ("/wjzyzx/004002/004002005/" in url) or ("/wjzyzx/004002/004002010/" in url):
        num = f1_click(driver, num)
        url = driver.current_url

    elif ("/wjzyzx/004003/004003002/004003002005/" in url) or ("/wjzyzx/004003/004003002/004003002007/" in url):
        num = f1_click(driver, num)
        url = driver.current_url

    elif ("/wjzyzx/004003/004003002/004003002008/" in url) or ("/wjzyzx/004003/004003002/004003002002/" in url):
        num = f1_click(driver, num)
        url = driver.current_url

    elif "/wjzyzx/004003/004003006/" in url:
        num = f1_click(driver, num)
        url = driver.current_url

    # 判断是否是第一次爬取，如果是增量更新,只获取前5页
    if num > CDC_NUM:
        return

    locator = (By.XPATH, "//ul[@class='ewb-notice-items']/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        cnum = re.findall(r'(\d+)/', str)[0]
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
            locator = (By.XPATH, "//ul[@class='ewb-notice-items']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@class='ewb-notice-items']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_="ewb-notice-items")

    trs = table.find_all("li", class_="clearfix")
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

        td = tr.find("span", class_="r ewb-date").text.strip()

        link = "http://www.ptfwzx.gov.cn"+link

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    # url = driver.current_url
    locator = (By.XPATH, "//ul[@class='ewb-notice-items']/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        driver.find_element_by_xpath("//td[@class='huifont']")
    except:
        num = f2_num(driver)
        driver.quit()
        return num

    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = re.findall(r'/(\d+)', str)[0]
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "ewb-route")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))

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


def f2_num(driver):
    global num_list,title_list
    num_list = []
    title_list = []
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    uls = soup.find_all('a', class_='block-link-more')
    total = len(uls)
    cnum = 0
    list_1 = []
    for i in range(1, int(total) + 1):
        locator = (By.XPATH, "(//a[@class='block-link'])[{}]".format(i))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        title_list.append(val)
        driver.find_element_by_xpath("(//a[@class='block-link-more'])[{}]".format(i)).click()
        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            num = int(re.findall(r'/(\d+)', str)[0])
        except:
            html_data = driver.page_source
            if "本栏目暂时没有内容" in html_data:
                num = 1
            else:
                num = 1
        cnum += num
        list_1.append(num)
        driver.back()

    for i in range(1, len(list_1) + 1):
        b = sum(list_1[:i])
        num_list.append(b)


    return int(cnum)



def f1_click(driver, num):
    url = driver.current_url
    list_num = int(len(num_list))
    for i in range(1, list_num+1):
        if i == 1:
            if num <= num_list[i-1]:
                num = num
                f1_data(driver, i)
                return num

        else:
            if num_list[i-2] < num <= num_list[i-1]:
                num = num - num_list[i-2]
                f1_data(driver, i)
                return num



def f1_data(driver, i):
    url = driver.current_url
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val = title_list[i-1]
        locator = (By.XPATH, "//div[@class='ewb-route']/span")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if val != str:
            url = url.rsplit('/', maxsplit=2)[0]
            driver.get(url)
            locator = (By.XPATH, "(//a[@class='block-link-more'])[{}]".format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            time.sleep(1)
            return
        else:
            return
    except:
        locator = (By.XPATH, "(//a[@class='block-link-more'])[{}]".format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        time.sleep(1)
        # url = driver.current_url
        # driver.get(url)
        return



data = [

    ["gcjs_zhaobiao_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002005/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_xianzhijia_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002006/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_jieguo_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002010/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002022/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_biangen_sheji_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002008/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zishenjieguo_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004002/004002023/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_zhaobiao_gongkai_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002005/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_yaoqing_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002006/004003002006007/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_jingzheng_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002007/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_yijia_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_xunjia_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002004/004003002004007/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003002/004003002008/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_gongkai_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006005/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_yaoqing_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006006/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_jingzheng_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006007/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_yijia_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_xunjia_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_danyilaiyuan_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003006/004003006008/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_biangen_gg",
     "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003004/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

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
    est_meta(conp,data=data,diqu="福建省莆田市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","putian"])

    # #
    # driver=webdriver.Chrome()
    # url = "http://www.ptfwzx.gov.cn/fwzx/wjzyzx/004003/004003004/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
