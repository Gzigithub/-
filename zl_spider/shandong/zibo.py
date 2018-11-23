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
    # print(num)
    url = driver.current_url
    if "CategoryNum" in url:
        url_1 = url.rsplit('/', maxsplit=2)[0]
        driver.get(url_1)
    try:
        locator = (By.XPATH, "(//table[@cellspacing='2']/tbody/tr[1]/td/a)[{}]".format(num))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    except:
        return
    href = driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(num)).click()
    # link = "http://www.dyggzyjy.gov.cn" + href
    # driver.get(link)
    locator = (By.XPATH, "//*[@id='MoreInfoList1_DataGrid1']/tbody/tr[1]/td[2]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    try:
        page_all = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/div[1]/font[2]/b').text
        page = page_all.strip()
    except:
        page = 1
    # 获取总页数
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



def f1_data(driver, num):
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/div[1]/font[3]/b').text)
    except Exception as e:
        cnum = 1
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text

    if num != cnum:
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        try:
            locator = (By.XPATH, "//*[@id='MoreInfoList1_DataGrid1']/tbody/tr[1]/td[2]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(2)

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("table", id="MoreInfoList1_DataGrid1")

    trs = tbody.find_all("tr")
    data = []
    for tr in trs:
        try:
            a = tr.find("a")
            td = tr.find_all("td")[2]
            tmp = [a["title"].strip(), td.text.strip(), "http://ggzyjy.zibo.gov.cn" + a["href"]]
            data.append(tmp)
        except:
            print("error_data")
            a = tr.find_all("td")[1]
            td = tr.find_all("td")[2]
            tmp = [a.text.strip(), td.text.strip(), ""]
            data.append(tmp)
            # print(tmp)

    return data




def f2(driver):

    locator = (By.XPATH, '(//td[@class="TDStyle"]/a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html = driver.page_source
    html_data = etree.HTML(html)
    page = html_data.xpath('(//font[@class="MoreinfoColor"])/text()')
    num = len(page)

    return int(num)



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
        ["gcjs_zhaobiao_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_zhongbiao_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_biangeng_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_zhaobiao_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_biangeng_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_gg","http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_yucai_gg", "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/",
         ["name", "ggstart_time", "href"]],


    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","zibo"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 5):
    #     df=f1(driver, i)
    #     print(df)
