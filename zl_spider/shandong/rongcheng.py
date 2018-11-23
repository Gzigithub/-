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
    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b')
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    if num != int(cnum):
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        # time.sleep(0.5)

        try:
            locator = (By.XPATH, "//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b[string()='%s']" % num)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(3)

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("table", id="MoreInfoList1_DataGrid1")

    trs = tbody.find_all("tr")
    data = []
    for tr in trs:
        a = tr.find("a")
        title = a['title']

        td = tr.find_all("td")
        span_1 = td[2].text.strip()
        # print(span_1)

        tmp = [title.strip(), span_1,"http://www.rcggzy.cn" + a["href"]]
        data.append(tmp)
        # print(tmp)

    df = pd.DataFrame(data=data)
    # print(df)
    return df




def f2(driver):

    locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = page_all.strip()


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
        "num": 15,

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg","http://www.rcggzy.cn/rcweb/004/004001/004001001/MoreInfo.aspx?CategoryNum=004001001",
         ["name", "ggstart_time", "href"]],

        ["gcjs_zuigaoxianjia_gg", "http://www.rcggzy.cn/rcweb/004/004001/004001002/MoreInfo.aspx?CategoryNum=004001002",
         ["name", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg","http://www.rcggzy.cn/rcweb/004/004001/004001003/MoreInfo.aspx?CategoryNum=004001003",
         ["name", "ggstart_time", "href"]],


        ["zfcg_zhaobiao_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004001/MoreInfo.aspx?CategoryNum=004002004001",
         ["name", "ggstart_time", "href"]],

        ["zfcg_biangeng_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004002/MoreInfo.aspx?CategoryNum=004002004002",
         ["name", "ggstart_time", "href"]],

        ["zfcg_zhongbiao_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004003/MoreInfo.aspx?CategoryNum=004002004003",
         ["name", "ggstart_time", "href"]],

        ["zfcg_xuqiu_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005001/MoreInfo.aspx?CategoryNum=004002005001",
         ["name", "ggstart_time", "href"]],

        ["zfcg_hetong_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005002/MoreInfo.aspx?CategoryNum=004002005002",
         ["name", "ggstart_time", "href"]],

        ["zfcg_hetong_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005003/MoreInfo.aspx?CategoryNum=004002005003",
         ["name", "ggstart_time", "href"]],

        ["qsydw_zhaobiao_gg", "http://www.rcggzy.cn/rcweb/004/004006/004006001/MoreInfo.aspx?CategoryNum=004006001",
         ["name", "ggstart_time", "href"]],

        ["qsydw_zhongbiao_gg", "http://www.rcggzy.cn/rcweb/004/004006/004006003/MoreInfo.aspx?CategoryNum=004006003",
         ["name", "ggstart_time", "href"]],

        ["qita_zhaobiao_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004001/MoreInfo.aspx?CategoryNum=004004001",
         ["name", "ggstart_time", "href"]],

        ["qita_biangeng_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004002/MoreInfo.aspx?CategoryNum=004004002",
         ["name", "ggstart_time", "href"]],

        ["qita_zhongbiao_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004003/MoreInfo.aspx?CategoryNum=004004003",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","rongcheng"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.rcggzy.cn/rcweb/004/004001/004001001/MoreInfo.aspx?CategoryNum=004001001"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
