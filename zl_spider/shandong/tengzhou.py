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
    locator = (By.XPATH, '(//td[@class="line2"]//a)[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall(r"_(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("_[0-9]*", "_1", url)
        else:
            s = "_%d" % (num) if num > 1 else "_1"
            url = re.sub("_[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//td[@class='line2']//a)[1][string()='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(3)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("td", class_="nr")
    trs = ul.find_all("td", class_="line2")
    data = []
    for li in trs:

        a = li.find("a")

        link = "http://www.tzccgp.gov.cn" + a["href"]
        try:
            span1 = li.find("td", width="12%").text
        except:
            span1 = ""

        tmp = [a.text.strip(), span1.strip(), link]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '(//td[@class="line2"]//a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "(//td[@class='f15']/span)[1]")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(r'共(\d+) 页', page_all)[0]
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
        ["zhaobiao_gg","http://www.tzccgp.gov.cn/list/?3_1.html",
         ["name", "ggstart_time", "href"]],

        ["zhongbiao_gg", "http://www.tzccgp.gov.cn/list/?4_1.html",
         ["name", "ggstart_time", "href"]],

        ["yanshou_gg", "http://www.tzccgp.gov.cn/list/?113_1.html",
         ["name", "ggstart_time", "href"]],

        ["hetong_gg", "http://www.tzccgp.gov.cn/list/?112_1.html",
         ["name", "ggstart_time", "href"]],

        ["xuqiu_gg", "http://www.tzccgp.gov.cn/list/?111_1.html",
         ["name", "ggstart_time", "href"]],

        ["biangeng_feibiao_gg", "http://www.tzccgp.gov.cn/list/?109_1.html",
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
    conp=["postgres","since2015","192.168.3.171","shandong","tengzhou"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.tzccgp.gov.cn/list/?3_3.html"
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
