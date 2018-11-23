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


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver, num):
    locator = (By.XPATH, "(//li[@class='lnWithData']/a)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        page_all = driver.find_element_by_xpath('//span[@class="td_Page"]').text
        cnum = re.findall(r'第(\d+)页', page_all)[0]
    except Exception as e:
        page_all = driver.find_element_by_xpath('//span[@class="td_Page"]').text
        cnum = re.findall(r'第(\d+)页', page_all)[0]
    val = driver.find_element_by_xpath('(//li[@class="lnWithData"]/a)[1]').text
    if num != int(cnum):
        driver.execute_script("javascript:pgTo({})".format(num-1))
        # time.sleep(0.5)
        try:
            locator = (By.XPATH, "(//li[@class='lnWithData']/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("ul", class_="infoList")

    trs = tbody.find_all("li", class_='lnWithData')
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            stat = tr.find('span').text.strip()
            state = re.findall(r'\[(.*)\]', stat)[0]
        except:
            state = ""
        span_1 = tr.find('span').text.strip()
        span_2 = re.findall(r'(\d+.*)', span_1)[0]

        tmp = [a.text.strip(), state, span_2, "http://jzggzy.jiaozhou.gov.cn/" + a["href"]]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    # print(df)
    return df




def f2(driver):

    locator = (By.XPATH, '//span[@class="td_Page"]')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = re.findall(r'共(\d+)页', page_all)[0]


    return int(page)



def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,
        "col": col,
        "conp": conp,
        "num": 10,

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?type=GJGG",
         ["name", "state", "ggstart_time", "href"]],


        ["gcjs_zhongbiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?regCode=&type=GJGS&subType=0",
         ["name", "state", "ggstart_time", "href"]],



        ["zfcg_zhaobiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?type=ZCGG",
         ["name", "state", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?regCode=&type=ZCGS&subType=0",
         ["name", "state", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","jiaozhou"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://jzggzy.jiaozhou.gov.cn/list.jsp?regCode=&type=ZCGG&subType=0"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(365, 367):
    #     df=f1(driver, i)
    #     print(df)
