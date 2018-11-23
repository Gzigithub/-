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
    locator = (By.XPATH, '//*[@id="1912"]/div/table[1]/tbody/tr/td[2]/span/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("pageNum=(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("pageNum=[0-9]*", "pageNum=1", url)
        else:
            s = "pageNum=%d" % (num) if num > 1 else "pageNum=1"
            url = re.sub("pageNum=[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        try:
            locator = (By.XPATH, "//*[@id='1912']/div/table[1]/tbody/tr/td[2]/span/a[string()='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(4)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="default_pgContainer")
    trs = ul.find_all("table")
    data = []
    for li in trs:

        a = li.find("a")
        title = a['title']
        link = "http://ggzy.rushan.gov.cn" + a["href"]
        try:
            span1 = li.find("span", class_="bt_time").text
        except:
            span1 = ""

        tmp = [title.strip(), span1.strip(), link]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '//*[@id="1912"]/div/table[1]/tbody/tr/td[2]/span/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@class='default_pgTotalPage']")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = page_all.strip()
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
        ["gcjs_zhaobiao_gg","http://ggzy.rushan.gov.cn/col/col1823/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href"]],

        ["gcjs_biangeng_gg", "http://ggzy.rushan.gov.cn/col/col1824/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg", "http://ggzy.rushan.gov.cn/col/col1825/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href"]],


        ["zfcg_biangeng_gg", "http://ggzy.rushan.gov.cn/col/col1827/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://ggzy.rushan.gov.cn/col/col1826/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://ggzy.rushan.gov.cn/col/col1828/index.html?uid=1912&pageNum=1",
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
    conp=["postgres","since2015","192.168.3.171","shandong","rushan"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzy.rushan.gov.cn/col/col1823/index.html"
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
