import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]





def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//div[@class="news-txt l"])[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("Paging=(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        locator = (By.XPATH, "//td[@class='huifont']")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall('(\d+)/', page_all)[0]
        if int(page) != num:
            time.sleep(5)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("table", id="DataList1")
    trs = ul.find_all("tr")
    data = []
    for li in trs:

        a = li.find("a")
        link = "http://www.rzggzyjy.gov.cn/rzwz/" + re.findall('../(.*)', a["href"])[0]
        try:
            span1 = li.find("div", class_="news-txt l").text
        except:
            span1 = ""
        try:
            span2 = li.find("div", class_="news-date r").text
        except:
            span2 = ""

        tmp = [span1.strip(), span2.strip(), link]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, "(//div[@class='news-txt l'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = re.findall('/(\d+)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    return int(page)


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 20,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg","http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001001&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["gcjs_biangeng_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001002&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001003&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["gcjs_liubiao_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001004&Paging=1",
         ["name", "ggstart_time", "href"]],


        ["zfcg_yuzhaobiao_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002001&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002002&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["zfcg_biangeng_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002003&Paging=1",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071002004&Paging=1",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
        print(data)
    for w in data:
        general_template(w[0], w[1], w[2], conp)


# conp = []

if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","rizhao"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.rzggzyjy.gov.cn/rzwz/ShowInfo/MoreJyxxList.aspx?categoryNum=071001001&Paging=1"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
