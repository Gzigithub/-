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
    # 获取当前页的url
    url = driver.current_url
    if "Paging" in url:
        # print(url)
        url_3 = url.rsplit('/', maxsplit=2)[0]
        # print(url_3)
        driver.get(url_3)
    try:
        locator = (By.XPATH, '//td[@class="subcatbel"]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    except:
        pass
    try:
        driver.find_element_by_xpath('(//tr[1]/td[@class="TDStyle"]/a)[{}]'.format(num)).text
    except:
        html = driver.page_source
        if "本栏目暂时没有内容" in html:
            time.sleep(1)
            return
    locator = (By.XPATH, '(//td[@class="subcatbel"]/a)[{}]'.format(num))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
    # url_link = driver.find_element_by_xpath('(//td[@class="MoreinfoColor"]/a)[{}]'.format(num)).click()
    # print(url)
    url_1 = driver.current_url
    # 获取当前页的url
    print(url_1)
    locator = (By.XPATH, '//*[@id="s-main"]/div/div[2]/div[2]/div[1]/h2')
    city = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    print(city)
    if "市辖区" in city:
        print("222")
        html = driver.page_source
        html_data = etree.HTML(html)
        page = html_data.xpath('//td[@class="subcatbel"]/a/text()')
        num = len(page)
        num = int(num)
        data_list = []
        for i in range(int(num) + 1):
            if i == 0:
                continue
            else:
                url_2 = driver.current_url
                if "Paging" in url_2:
                    # print(url)
                    url_3 = url_2.rsplit('/', maxsplit=2)[0]
                    # print(url_3)
                    driver.get(url_3)
                locator = (By.XPATH, '(//td[@class="subcatbel"]/a)[{}]'.format(i))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
                time.sleep(1)
                html = driver.page_source
                if "本栏目信息正在更新中" in html:
                    time.sleep(1)
                    return
                locator = (By.XPATH, '(//a[@class="WebList_sub"])[1]')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                page_num = driver.find_element_by_xpath('//td[@class="huifont"]').text
                # 获取总页数
                page = re.findall(r'/(\d+)', page_num)[0]
                # print(page)
                for j in range(int(page) + 1):
                    if j == 0:
                        continue
                    else:
                        df = f1_data(driver, j)
                        data_list.append(df)

        data = []
        for i in data_list:
            for j in i:
                data.append(j)

        driver.get(url)
        df = pd.DataFrame(data=data)
        # print(df)
        return df

    else:
        print("1111")
        locator = (By.XPATH, '(//a[@class="WebList_sub"])[1]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        page_num = driver.find_element_by_xpath('//td[@class="huifont"]').text
        # print(page_num)
        # 获取总页数
        page = re.findall(r'/(\d+)', page_num)[0]
        # print(page)
        data_list = []
        for i in range(int(page) + 1):
            if i == 0:
                continue
            else:
                # print(i)
                df = f1_data(driver, i)
                # print(df)
                data_list.append(df)
        # print(data_list)

        data = []
        for i in data_list:
            for j in i:
                data.append(j)

        df = pd.DataFrame(data=data)
        # print(df)
        return df


def f1_data(driver, i):
    url_i = driver.current_url
    # print(url_i)
    if "Paging" not in url_i:
        # print(url)
        url_2 = url_i.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        url_1 = url_2 + "/?Paging={}".format(i)
        # print(url_1)
        driver.get(url_1)
    else:
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(i), url_i)
        val = driver.find_element_by_xpath('//*[@id="right_table"]/table/tbody/tr[1]/td[2]/a').text
        # print(url_1)
        driver.get(url_1)
        locator = (By.XPATH, "//*[@id='right_table']/table/tbody/tr[1]/td[2]/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, '(//a[@class="WebList_sub"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("div", id="right_table")
    # tb = ul.find_all("table",recursive=False)[0]
    lis = ul.find_all("tr", height='30')
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://www.taggzyjy.com.cn" + a["href"]
        span = li.find("td", width='80').text.strip()
        span_1 = re.findall(r"\[(.*)\]", span)[0]
        tmp = [title, span_1, link]
        data.append(tmp)


    return data




def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """

    locator = (By.XPATH, '//td[@class="subcatbel"]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    html_data = etree.HTML(html)
    page = html_data.xpath('//td[@class="subcatbel"]/a/text()')
    num = len(page)

    return int(num)


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 15,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [

        ["gcjs_zhaobiao_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_zhongbiao_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/",
         ["name", "ggstart_time", "href"]],
        ["gcjs_biangeng_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhaobiao_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/",
         ["name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/",
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
    conp=["postgres","since2015","192.168.3.171","shandong","taian"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(2,4):
    #     df=f1(driver, i)
    #     print(df)
