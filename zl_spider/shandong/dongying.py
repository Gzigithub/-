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
    print(num)
    url = driver.current_url
    if "CategoryNum" in url:
        url_1 = url.rsplit('/', maxsplit=2)[0]
        driver.get(url_1)

    locator = (By.XPATH, '//td[@class="white"]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    print(val)
    str = driver.find_element_by_xpath('(//td[@class="MoreinfoColor"])[{}]'.format(num)).text
    # val_2 = str.strip('【').strip("】")
    print(str)
    if val != str:
        href = driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(num)).click()
        # link = "http://www.dyggzyjy.gov.cn" + href
        # driver.get(link)
        locator = (By.XPATH, "//td[@class='white'][string()='%s']" % str)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    if "暂时无此类项目" in html:
        url_s = driver.current_url
        url_3 = url_s.rsplit('/', maxsplit=2)[0]
        print(url_3)
        driver.get(url_3)
        time.sleep(1)
        return
    if "更多信息" in html:
        driver.find_element_by_xpath("//td[@align='right']/a | //td[@colspan='3']/a").click()
        locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        page = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b').text
        # 获取总页数
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



def f1_data(driver, num):
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text)
    except StaleElementReferenceException:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text)
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
    if num != cnum:
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        time.sleep(0.5)
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
            tmp = [a["title"], td.text.strip(), "http://www.dyggzyjy.gov.cn" + a["href"]]
            data.append(tmp)
        except:
            a = tr.find_all("td")[1]
            td = tr.find_all("td")[2]
            tmp = [a.text.strip(), td.text.strip(), ""]
            data.append(tmp)
            # print(tmp)

    return data




def f2(driver):
    locator = (By.XPATH, '//*[@id="TD004002001"]/table/tbody/tr/td/a')
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
        ["gcjs_zhaobiao_gg","http://www.dyggzyjy.gov.cn/dysite/004/004001/004001001/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_zhongbiao_gg","http://www.dyggzyjy.gov.cn/dysite/004/004001/004001003/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_gg","http://www.dyggzyjy.gov.cn/dysite/004/004001/004001004/",
         ["name", "ggstart_time", "href"]],

        ["gcjs_qita_gg","http://www.dyggzyjy.gov.cn/dysite/004/004001/004001005/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_zhaobiao_gg","http://www.dyggzyjy.gov.cn/dysite/004/004002/004002001/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_b_gg","http://www.dyggzyjy.gov.cn/dysite/004/004002/004002002/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_gg","http://www.dyggzyjy.gov.cn/dysite/004/004002/004002003/",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","dongying"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.dyggzyjy.gov.cn/dysite/004/004001/004001003/004001003004/MoreInfo.aspx?CategoryNum=004001003004"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(3, 8):
    #     df=f1_data(driver, 47)
    #     print(df)
