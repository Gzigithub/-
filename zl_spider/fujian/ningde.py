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

_name_="ningde"


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
    url = driver.current_url
    try:
        locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        val = title_list[i-1]
        locator = (By.XPATH, "//div[@class='ewb-route']/a[4]")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if val != str:
            driver.find_element_by_xpath("//ul[@class='ewb-left-items']/li[1]/a").click()

            locator = (By.XPATH, "(//a[@class='block-link l'])[1]")
            tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

            locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            locator = (By.XPATH, "(//a[@class='block-link l'])[1][not(contains(string(), '{}'))]".format(tar))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

            locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(j))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            time.sleep(1)
            return
        else:
            return
    except:
        locator = (By.XPATH, "(//a[@class='block-link l'])[1]")
        tar = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

        locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(i))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        locator = (By.XPATH, "(//a[@class='block-link l'])[1][not(contains(string(), '{}'))]".format(tar))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        time.sleep(1)
        return



def zfcg_data(driver, num):
    url = driver.current_url
    locator = (By.XPATH, "//table[@class='table table-hover dataTables-example']/tbody/tr[1]/td/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//button[@class='active']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = int(str)
    except:
        cnum = 1
    try:
        notice_type = re.findall(r'notice_type=(.*)&', url)[0]
    except:
        notice_type = re.findall(r'notice_type=(.*)', url)[0]

    if num != int(cnum):
        driver.execute_script("javascript:location.href='?page={0}&notice_type={1}'".format(num, notice_type))
        # driver.execute_script("javascript:location.href='?page=6&notice_type=7dc00df822464bedbf9e59d02702b714'")
        try:
            locator = (By.XPATH,
                       "//table[@class='table table-hover dataTables-example']/tbody/tr[1]/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH,
                       "//table[@class='table table-hover dataTables-example']/tbody/tr[1]/td/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find("table", class_="table table-hover dataTables-example")
    tbody = table.find('tbody')

    trs = tbody.find_all("tr", class_="gradeX")
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
        td = tr.find_all("td")[4].text.strip()
        link = "http://www.ndzfcg.gov.cn" + link.strip()
        tmp = [title, td, link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f1(driver, num):
    url = driver.current_url
    if "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/" in url:
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

    if "http://www.ndzfcg.gov.cn/350900/noticelist/" in url:
        df = zfcg_data(driver, num)
        return df

    locator = (By.XPATH, "//ul[@class='ewb-right-itemss']/li[1]/a")
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
            locator = (By.XPATH, "//ul[@class='ewb-right-itemss']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//ul[@class='ewb-right-itemss']/li[1]/a[not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("ul", class_="ewb-right-itemss")

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

        td = tr.find("span", class_='ewb-ndate r').text.strip()

        link = "http://www.ndggzy.gov.cn:8090"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    url = driver.current_url
    if "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/" in url:
        global j
        j = 0
        j = int(re.findall(r'info=(\d+)', url)[0])
        url = url.rsplit('/', maxsplit=1)[0]
        # print(url)
        driver.get(url)
        num = f2_num(driver, j)
        driver.quit()
        return num

    elif "http://www.ndzfcg.gov.cn" in url:
        locator = (By.XPATH, "//button[@class='active']")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, "//div[@class='pageGroup']/button[last()]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        try:
            locator = (By.XPATH, "//button[@class='active'][not(contains(string(),'%s'))]" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            locator = (By.XPATH, "//button[@class='active']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            num = int(str)
        except:
            num = 1

        driver.quit()
        return int(num)


    else:
        locator = (By.XPATH, "//ul[@class='ewb-right-itemss']/li[1]/a")
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
    lis = soup.find_all('a', class_="block-link l")
    total = len(lis)
    cnum = 0
    list_1 = []
    locator = (By.XPATH, "(//a[@class='block-link l'])[1]")
    val_1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    for i in range(1, int(total) + 1):
        locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(i))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        # print(val)
        title_list.append(val)
        driver.find_element_by_xpath("(//a[@class='block-link l'])[{}]".format(i)).click()

        locator = (By.XPATH, "(//a[@class='block-link l'])[1][not(contains(string(), '{}'))]".format(val_1))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        time.sleep(1)

        locator = (By.XPATH, "(//a[@class='block-link l'])[{}]".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        try:
            locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
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
        locator = (By.XPATH, "//li[@class='current ewb-haschild']/a".format(j))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

    for i in range(1, len(list_1) + 1):
        b = sum(list_1[:i])
        num_list.append(b)


    return int(cnum)



def f3(driver, url):

    driver.get(url)
    if "http://www.ndzfcg.gov.cn/" in url:
        locator = (By.CLASS_NAME, "notice")
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

        div = soup.find('div', id="print-content")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div


    locator = (By.CLASS_NAME, "ewb-topbar")
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

    div = soup.find('div', class_="article-block")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_fangwu_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/info=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_shuli_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/info=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_shizheng_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/info=3",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_jiaotong_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/info=4",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_qita_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006001/info=5",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006002/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_jieguo_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006005/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_zhaobiao_gg",
     "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=463fa57862ea4cc79232158f5ed02d03&purchase_item_name=",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?page=1&notice_type=7dc00df822464bedbf9e59d02702b714&",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_jieguo_gg",
     "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?page=21&notice_type=b716da75fe8d4e4387f5a8c72ac2a937&",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_biangen_jieguo_gg",
     "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=d812e46569204c7fbd24cbe9866d0651&purchase_item_name=",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg",
     "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=255e087cf55a42139a1f1b176b244ebb&purchase_item_name=",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zhaobiao_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/jyxx/012001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["jieguo_gg",
     "http://www.ndggzy.gov.cn:8090/ndztb/jyxx/012002/",
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
    est_meta(conp,data=data,diqu="福建省宁德市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","ningde"])

    #
    # driver=webdriver.Chrome()
    # url = "http://www.ndzfcg.gov.cn/350900/noticelist/d03180adb4de41acbb063875889f9af1/?page=1&notice_type=7dc00df822464bedbf9e59d02702b714&"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "http://www.ndggzy.gov.cn:8090/ndztb/gcjy/006004/"
    # driver.get(url)
    # for i in range(3, 7):
    #     df=f1(driver, i)
    #     print(df)