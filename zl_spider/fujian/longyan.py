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

_name_="longyan"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


num_list = []
title_list = []
j=0



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
    try:
        locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val = title_list[i-1]
        locator = (By.XPATH, "//div[@class='container']/p/a[4]")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if val != str:
            driver.find_element_by_xpath("//ul[@class='wb-tree']/li[2]/h3/a").click()

            locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[1]/div[1]/span/a")
            tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

            locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[1]/div[1]/span/a[not(contains(string(), '{}'))]".format(tar))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(j))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            time.sleep(1)
            return
        else:
            return
    except:
        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[1]/div[1]/span/a")
        tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[1]/div[1]/span/a[not(contains(string(), '{}'))]".format(tar))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        time.sleep(1)
        return


def f1(driver, num):
    url = driver.current_url
    if "https://www.lyggzy.com.cn/lyztb/gcjs/081008/" in url:
        if "info" in url:
            # j = int(re.findall(r'info=(\d+)', url)[0])
            url = url.rsplit('/', maxsplit=1)[0]
            # print(url)
            driver.get(url)
        num = f1_click(driver, num, j)
        url = driver.current_url


    # 判断是否是第一次爬取，如果是增量更新,只获取前5页
    if num > CDC_NUM:
        return

    locator = (By.XPATH, "//ul[@class='list']/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1


    if num != int(cnum):
        driver.execute_script("ShowAjaxNewPage(window.location.pathname,'categorypagingcontent',{})".format(num))

        try:
            locator = (By.XPATH, "//ul[@class='list']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@class='list']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_="list")

    trs = table.find_all("li", class_="list-item clearfix")
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

        td = tr.find("span", class_='list-date').text.strip()

        link = "https://www.lyggzy.com.cn"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    url = driver.current_url

    if "https://www.lyggzy.com.cn/lyztb/gcjs/081008/" in url:
        global j
        j = 0
        j = int(re.findall(r'info=(\d+)', url)[0])
        url = url.rsplit('/', maxsplit=1)[0]
        # print(url)
        driver.get(url)
        num = f2_num(driver, j)
        driver.quit()
        return num
    else:
        locator = (By.XPATH, "//ul[@class='list']/li[1]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            num = re.findall(r'/(\d+)', str)[0]
        except:
            num = 1
        driver.quit()
        return int(num)


def f2_num(driver, j):
    global num_list,title_list
    num_list = []
    title_list = []
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    uls = soup.find('div', id="categorypagingcontent")
    lis = uls.find_all('a', style="color:#333; font-size:16px")
    total = len(lis)
    cnum = 0
    list_1 = []
    for i in range(1, int(total) + 1):
        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/span/a".format(i))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

        title_list.append(val)
        driver.find_element_by_xpath("//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(i)).click()

        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[1]/div[1]/span/a[not(contains(string(), '{}'))]".format(val))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        time.sleep(1)

        locator = (By.XPATH, "//*[@id='categorypagingcontent']/div[{}]/div[1]/div/a".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        try:
            locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
            str = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).text
            num = int(re.findall(r'/(\d+)', str)[0])
        except:
            html_data = driver.page_source
            if "本栏目暂时没有内容" in html_data:
                num = 1

        cnum += num
        list_1.append(num)
        locator = (By.XPATH, "//ul[@class='wb-tree']/li[2]/h3/a".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

    for i in range(1, len(list_1) + 1):
        b = sum(list_1[:i])
        num_list.append(b)


    return int(cnum)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "bg")
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

    div = soup.find('div', class_="detail-content")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_yifajinchang_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001003/081001003001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_qita_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001003/081001003002/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001009/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001010/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081001/081001005/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_quxian_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081008/info=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_quxian_gg",
     "https://www.lyggzy.com.cn/lyztb/gcjs/081008/info=3",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_yucai_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003007/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yucai_qita_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003007/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_qita_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_qita_gg",
     "https://www.lyggzy.com.cn/lyztb/zfcg/082003/082003002/",
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
    est_meta(conp,data=data,diqu="福建省龙岩市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","longyan"])


    # driver=webdriver.Chrome()
    # url = "https://www.lyggzy.com.cn/lyztb/gcjs/081008/info=3"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "https://www.lyggzy.com.cn/lyztb/gcjs/081008/info=3"
    # driver.get(url)
    # for i in range(22, 28):
    #     df=f1(driver, i)
    #     print(df)