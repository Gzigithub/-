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
    locator = (By.XPATH, '(//span[@class="info-name"])[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("Paging=(.*)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//span[@class='info-name'])[1]").text
        # print(url)
        driver.get(url)
        # time.sleep(1)
        # print("1111")
        locator = (By.XPATH, "(//span[@class='info-name'])[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        # print("22222")

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="info-form")
    tbody = ul.find('tbody')
    trs = tbody.find_all("tr")
    data = []
    for li in trs:
        try:
            info_number = li.find("span", class_="info-number").text
        except:
            info_number = ""
        a = li.find("a")
        link = "http://ggzy.weifang.gov.cn" + a["href"]
        try:
            span1 = li.find_all("span", class_="info-date")[0].text
        except:
            span1 = ""
        try:
            span2 = li.find_all("span", class_="info-date")[1].text
        except:
            span2 = ""
        try:
            state = li.find_all("span", class_="state current")[0].text
        except:
            state = ""
        tmp = [info_number.strip(), a.text.strip(), span1.strip(), span2.strip(), link, state.strip()]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '(//span[@class="info-name"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = re.findall('/(.*)', page_all)[0]
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
        # ["gcjs_zhaobiao_gg",
        # "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012001&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["gcjs_biangeng_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012002&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["gcjs_dayi_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012005&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["gcjs_zhongbiaohx_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012006&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["gcjs_zhongbiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012007&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["gcjs_liubiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_ggycgg.aspx?address=&type=&categorynum=004012010&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        #
        ["gcjs_danyilaiyuan_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012008&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],


        # ["zfcg_zhaobiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg_cgxq.aspx?address=&categorynum=004002017&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_zhongbiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?address=&type=&categorynum=004002001&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_biangeng_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002011&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_zhongbiaoshencha_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002012&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_liubiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002016&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_zhongzhi_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002015&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        #
        # ["zfcg_yanshou_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002014&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["zfcg_caigouhetong_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002013&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        #
        # ["ylsb_zhaobiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006001&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["ylsb_biangeng_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006002&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["ylsb_zhongbiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006003&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["ylsb_yanshou_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006007&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        # ["ylsb_liubiao_gg",
        #  "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006008&Paging=1",
        #  ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],

        ["qsydw_zhaobiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007001&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        ["qsydw_biangeng_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007004&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        ["qsydw_zhongbiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007002&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        ["qsydw_zhongzhi_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007007&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],
        ["qsydw_liubiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007009&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "state"]],

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
    conp=["postgres","since2015","192.168.3.171","shandong","weifang"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg_cgxq.aspx?address=001&categorynum=004002017&Paging=118"
    # driver.get(url)
    # for i in range(1, 10):
    #     df=f1(driver, 1)
    #     print(df)
