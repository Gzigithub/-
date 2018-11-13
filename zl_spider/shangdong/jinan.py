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
    locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = driver.find_element_by_xpath('//*[@id="pag"]').text

    # val = driver.find_element_by_xpath("//ul[@class='ewb-info-list']//li[1]//a").text
    if cnum != num:
        driver.find_element_by_xpath('//*[@id="toPageNum"]').clear()
        driver.find_element_by_xpath('//*[@id="toPageNum"]').send_keys(num)
        driver.find_element_by_xpath('//*[@id="part4"]/span[8]').click()
        locator = (By.XPATH, "//*[@id='content']/ul/li[1]/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", id="content")
    lis = ul.find_all("li")
    data = []
    for li in lis:
        a = li.find("a")
        title = a["title"]
        try:
            a_nunm = a["onclick"]
            a_num = re.findall('\((.*)\)', a_nunm)[0]
            link = "http://jnggzy.jinan.gov.cn/jnggzyztb/front/showNotice.do?iid={}&xuanxiang=".format(a_num)
        except:
            link = "http://jnggzy.jinan.gov.cn" + a["href"]

        span1 = li.find("span", class_="span1")
        span2 = li.find("span", class_="span2")
        tmp = [span1.text.strip(), title.strip(), span2.text.strip(), link]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//*[@id="apagesum"]')
        page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
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
        ["gcjs_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["gcjs_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["zfcg_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=3&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["zfcg_feibiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=4&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["qtxm_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=7&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href"]],
        ["qtxm_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=7&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href"]],
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
    conp=["postgres","since2015","192.168.3.171","shandong","jinan"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=7&xuanxiang=2&area="
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f1(driver, i)
    #     print(df)
