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
    locator = (By.XPATH, '(//td[@class="box_td"]/a)[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("pageIndex=(.*)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("pageIndex=[0-9]*", "pageIndex=1", url)
        else:
            s = "pageIndex=%d" % (num) if num > 1 else "pageIndex=1"
            url = re.sub("pageIndex=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//td[@class='box_td']/a)[1]").text
        # print(url)
        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, "(//td[@class='box_td']/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        # print("22222")

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="info_con")
    trs = ul.find_all("tr")
    data = []
    for li in trs:
        td = li.find("td", class_="box_td")
        a = td.find("a")
        link = "http://202.110.193.29:10000" + a["href"]

        span2 = li.find_all("td")[1]

        tmp = [a.text.strip(), span2.text.strip(), link]
        data.append(tmp)
        # print(data)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '(//td[@class="box_td"]/a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//div[@class="pages"]/a[last()]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        url = driver.current_url
        # print(url)
        page = int(re.findall("pageIndex=(.*)", url)[0])
        # page = re.findall('/(.*)', page_all)[0]
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
        "num": 10,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-0?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["gcjs_zigeshencha_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-4?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["gcjs_yuzhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-2?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["gcjs_feibiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-3?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["gcjs_zhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-8?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["gcjs_jiaoyijincheng_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-9?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhaobiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-0?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-5?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-2?pageIndex=1",
         ["name", "ggstart_time", "href"]],
        ["zfcg_feibiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-3?pageIndex=1",
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
    conp=["postgres","since2015","192.168.3.171","shandong","qingdao"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-4?pageIndex=1"
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f2(driver)
    #     print(df)
