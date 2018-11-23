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
    n = 5
    df = f1_data(driver, num, n)
    return df

def f1_data(driver, num, n):
    url = driver.current_url
    locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
    li_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    locator = (By.XPATH, "//li[@class='current']")
    li_class_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # print(li_name)
    # print(li_class_name)
    if li_name != li_class_name:
        locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        time.sleep(0.8)
    try:
        locator = (By.XPATH, '//*[@id="ContentPlaceHolder1_lblCurrent{}"]'.format(n))
        cnum = WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator)).text
    except:
        time.sleep(1)
        locator = (By.XPATH, '//*[@id="ContentPlaceHolder1_lblCurrent{}"]'.format(n))
        cnum = WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator)).text

    val = driver.find_element_by_xpath('//*[@id="contentL{}"]/div/ul/li[1]/a/h2'.format(n)).text
    if num != int(cnum):
        while True:
            url_1 = driver.current_url
            if url_1 != url:
                driver.back()
                # locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
                # WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            if num > int(cnum):
                locator = (By.XPATH, "//a[@id='ContentPlaceHolder1_lbtnDown{}']".format(n))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            else:
                locator = (By.XPATH, "//a[@id='ContentPlaceHolder1_lbntUp{}']".format(n))
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

            url_1 = driver.current_url
            if url_1 != url:
                driver.back()
            locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            url_1 = driver.current_url
            if url_1 != url:
                driver.back()
            time.sleep(0.8)
            locator = (By.XPATH, '//*[@id="ContentPlaceHolder1_lblCurrent{}"]'.format(n))
            cn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            if int(cn) == num:
                break


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("div", id="contentL{}".format(n))

    trs = tbody.find_all("li")
    data = []
    for tr in trs:
        a = tr.find("a")
        title = tr.find("h2")
        try:
            stat = tr.find('div', class_='info_right')
            span = stat.find_all("em")
            # place = span[0].text.strip()
            date = span[1].text.strip()
        except:
            # place = ""
            date = ''
        # span_1 = tr.find('span').text.strip()
        # span_2 = re.findall(r'(\d+.*)', span_1)[0]

        tmp = [title.text.strip(), date, "http://hzsggzyjy.gov.cn/" + a["href"]]
        # print(tmp)
        data.append(tmp)

    df = pd.DataFrame(data=data)
    # print(df)
    return df





def f2(driver):
    n = 5
    num = f2_data(driver, n)
    return num

def f2_data(driver, n):
    locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
    li_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    locator = (By.XPATH, "//li[@class='current']")
    li_class_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # print(li_name)
    # print(li_class_name)
    if li_name != li_class_name:
        locator = (By.XPATH, "//*[@id='tabL{}']".format(n))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        time.sleep(2)
    locator = (By.XPATH, "//span[@id='ContentPlaceHolder1_lblTotal{}']".format(n))
    page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

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
        "num": 1,

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg","http://hzsggzyjy.gov.cn/cityInfoList.aspx?s=1&t=1",
         ["name", "ggstart_time", "href"]],

        ["qsydw_zhaobiao_gg", "http://hzsggzyjy.gov.cn/cityInfoList.aspx?s=1&t=5",
         ["name", "ggstart_time", "href"]],

        ["qita_zhaobiao_gg", "http://hzsggzyjy.gov.cn/cityInfoList.aspx?s=1&t=6",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","heze"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://hzsggzyjy.gov.cn/cityInfoList.aspx?s=1&t=1"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
