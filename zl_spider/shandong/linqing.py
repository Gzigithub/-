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
        html = driver.page_source
        html_data = etree.HTML(html)
        data = html_data.xpath('//div[@class="content"]//tr[1]//a/text()')
        nume = int(len(data))
        print(nume)
        if nume == 1:
            print("qqq")
            data = f1_data(driver, num)
            df = pd.DataFrame(data=data)
            # print(df)
            return df
        else:
            # print(url)
            url_3 = url.rsplit('/', maxsplit=2)[0]
            # print(url_3)
            driver.get(url_3)

    # 获取当前页的url
    locator = (By.XPATH, '(//td[@class="MoreinfoColor"]/a)[{}]'.format(num))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
    # url_link = driver.find_element_by_xpath('(//td[@class="MoreinfoColor"]/a)[{}]'.format(num)).click()
    # print(url)
    try:
        locator = (By.XPATH, '//div[@class="content"]//tr[1]//a')
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
    except:
        html = driver.page_source
        if "本栏目暂时没有内容" in html:
            url_s = driver.current_url
            url_3 = url_s.rsplit('/', maxsplit=2)[0]
            print(url_3)
            driver.get(url_3)
            time.sleep(1)
            return

    page_num = driver.find_element_by_xpath('//td[@class="huifont"]').text
    # 获取总页数
    page = re.findall('/(\d+)', page_num)[0]
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

    url = driver.current_url
    url_3 = url.rsplit('/', maxsplit=2)[0]
    # print(url_3)
    driver.get(url_3)
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
    nume = driver.find_element_by_xpath('//td[@class="huifont"]').text
    # 获取总页数
    cnum = re.findall(r'(\d+)/', nume)[0]
    if i != int(cnum):
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(i), url_i)
        val = driver.find_element_by_xpath('//div[@class="content"]//tr[1]//a').text
        # print(url)
        driver.get(url_1)
        try:
            locator = (By.XPATH, "//div[@class='content']//tr[1]//a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(3)

    # print(url_1)
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("div", class_="content")
    tb = ul.find_all("div",recursive=False)[0]
    lis = tb.find_all("tr")
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://ggzy.linqing.gov.cn" + a["href"]
        span = li.find("font")
        tmp = [title.strip(), span.text.strip(), link]
        data.append(tmp)


    return data




def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    url = driver.current_url
    if "Paging=1" in url:
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # 获取总页数
        num = re.findall(r'/(\d+)', page_num)[0]
    else:
        locator = (By.XPATH, '//td[@class="MoreinfoColor"]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        html = driver.page_source
        html_data = etree.HTML(html)
        page = html_data.xpath('//td[@class="MoreinfoColor"]/a/text()')
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
        "num": 10,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        # ["gcjs_zhaobiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["gcjs_biangeng_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001002/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["gcjs_zhongbiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001003/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["gcjs_yucai_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001004/",
        #  ["name", "ggstart_time", "href"]],


        ["zfcg_zhaobiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002001/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_biangeng_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002002/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002003/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_liubiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002004/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_danyilaiyuan_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006006/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["zfcg_yucai_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079002/079002006/079002006001/?Paging=1",
         ["name", "ggstart_time", "href"]],


        ["ylcg_zhaobiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005001/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["ylcg_biangeng_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005002/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["ylcg_zhongbiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079005/079005003/?Paging=1",
         ["name", "ggstart_time", "href"]],



        ["qsydw_zhaobiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006001/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_biangeng_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006002/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_zhongbiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006003/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_liubiao_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006004/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_yucai_gg", "http://ggzy.linqing.gov.cn/lqweb/jyxx/079006/079006005/?Paging=1",
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
    conp=["postgres","since2015","192.168.3.171","shandong","linqing"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzy.linqing.gov.cn/lqweb/jyxx/079001/079001001/"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1,4):
    #     df=f1(driver, i)
    #     print(df)
