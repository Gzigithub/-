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
    locator = (By.XPATH, '(//ul[@class="article-list2"]/li/div/a)[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "index.jhtml" in url:
        url = re.sub("index", "index_1", url)
        driver.get(url)
    cnum = int(re.findall("index_(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(' (\d+)/', page_all)[0]
        if int(page) != num:
            time.sleep(5)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("ul", class_="article-list2")
    trs = ul.find_all("li")
    data = []
    for li in trs:

        a = li.find("a")
        link = "http://www.whggzyjy.cn" + a["href"]
        try:
            span1 = li.find_all("div", class_="list-times")[0].text
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
    locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
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
        ["gcjs_zhaobiao_gg","http://www.whggzyjy.cn/jyxxzbxm/index.jhtml",["name", "ggstart_time", "href"]],

        ["gcjs_zigeshencha_gg", "http://www.whggzyjy.cn/jyxxzbgg/index.jhtml", ["name", "ggstart_time", "href"]],

        ["gcjs_kaibiaojilu_gg", "http://www.whggzyjy.cn/jyxxkbjl/index.jhtml", ["name", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg", "http://www.whggzyjy.cn/jyxxzbgs/index.jhtml", ["name", "ggstart_time", "href"]],

        ["gcjs_zbwenjianchengqin_gg", "http://www.whggzyjy.cn/jyxxzbwj/index.jhtml", ["name", "ggstart_time", "href"]],

        ["zfcg_yuzhaobiao_gg", "http://www.whggzyjy.cn/jyxxcgxq/index.jhtml", ["name", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://www.whggzyjy.cn/jyxxcggg/index.jhtml", ["name", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://www.whggzyjy.cn/jyxxcjgg/index.jhtml", ["name", "ggstart_time", "href"]],

        ["zfcg_caigouhetong_gg", "http://www.whggzyjy.cn/jyxxcght/index.jhtml", ["name", "ggstart_time", "href"]],

        ["zfcg_yanshou_gg", "http://www.whggzyjy.cn/jyxxysbg/index.jhtml", ["name", "ggstart_time", "href"]],

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
    conp=["postgres","since2015","192.168.3.171","shandong","weihai"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.whggzyjy.cn/jyxxgcjs/index.jhtml"
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
