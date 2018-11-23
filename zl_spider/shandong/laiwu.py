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

    if ("CategoryNum=044004001" in url) or ("CategoryNum=044004003" in url) or ("CategoryNum=044004002" in url):
        data = f1_data(driver, num)
        df = pd.DataFrame(data=data)
        # print(df)
        return df
    elif ("CategoryNum=044001001001" in url) or ("CategoryNum=044001001002" in url) or ("CategoryNum=044001001003" in url) or ("CategoryNum=044001001004" in url) or ("CategoryNum=044001001005" in url):
        data = f1_data(driver, num)
        df = pd.DataFrame(data=data)
        # print(df)
        return df
    elif ("CategoryNum=044001002001" in url) or ("CategoryNum=044001002002" in url) or ("CategoryNum=044001002003" in url) or ("CategoryNum=044001002004" in url) or ("CategoryNum=044001002005" in url):
        data = f1_data(driver, num)
        df = pd.DataFrame(data=data)
        # print(df)
        return df
    elif ("CategoryNum=044001003002" in url) or ("CategoryNum=044001003003" in url) or ("CategoryNum=044001003004" in url):
        data = f1_data(driver, num)
        df = pd.DataFrame(data=data)
        # print(df)
        return df
    else:
        if "CategoryNum" in url:
            url_1 = url.rsplit('/', maxsplit=2)[0]
            driver.get(url_1)

        locator = (By.XPATH, "(//table[@cellspacing='3']/tbody/tr[1]/td/a['title'])[{}]".format(num))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        print(val)
        href = driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(num)).click()
        # link = "http://www.dyggzyjy.gov.cn" + href
        # driver.get(link)
        locator = (By.XPATH, "(//td[@align='left' and @width='602']/a['title'])[1]")
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
            tal = driver.find_element_by_xpath("(//td[@align='left' and @width='602']/a['title'])[1]").text
            driver.find_element_by_xpath("//td[@align='right']/a | //td[@colspan='3']/a").click()

            locator = (By.XPATH, "//*[@id='MoreInfoList1_DataGrid1']/tbody/tr[1]/td[2]/a")
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
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text.strip())
    except StaleElementReferenceException:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text.strip())
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
            tmp = [a.text.strip(), td.text.strip(), "http://ggzy.laiwu.gov.cn" + a["href"]]
            data.append(tmp)
        except:
            a = tr.find_all("td")[1]
            td = tr.find_all("td")[2]
            tmp = [a.text.strip(), td.text.strip(), ""]
            data.append(tmp)
            # print(tmp)

    return data




def f2(driver):
    url = driver.current_url
    if ("CategoryNum=044004001" in url) or ("CategoryNum=044004002" in url) or ("CategoryNum=044004003" in url):
        locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    elif ("CategoryNum=044001001001" in url) or ("CategoryNum=044001001002" in url) or (
            "CategoryNum=044001001003" in url) or ("CategoryNum=044001001004" in url) or (
            "CategoryNum=044001001005" in url):
        locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    elif ("CategoryNum=044001002001" in url) or ("CategoryNum=044001002002" in url) or (
            "CategoryNum=044001002003" in url) or ("CategoryNum=044001002004" in url) or (
            "CategoryNum=044001002005" in url):
        locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    elif ("CategoryNum=044001003002" in url) or ("CategoryNum=044001003003" in url) or (
            "CategoryNum=044001003004" in url):
        locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    else:
        locator = (By.XPATH, '(//a[@target="_blank"])[2]')
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
        "num": 15,

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_kancha_zhaobiao_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001001/044001001001/MoreInfo.aspx?CategoryNum=044001001001",
         ["name", "ggstart_time", "href"]],
        ["gcjs_jianli_zhaobiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001001/044001001002/MoreInfo.aspx?CategoryNum=044001001002",
         ["name", "ggstart_time", "href"]],
        ["gcjs_shigong_zhaobiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001001/044001001003/MoreInfo.aspx?CategoryNum=044001001003",
         ["name", "ggstart_time", "href"]],
        ["gcjs_huowu_zhaobiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001001/044001001004/MoreInfo.aspx?CategoryNum=044001001004",
         ["name", "ggstart_time", "href"]],
        ["gcjs_qita_zhaobiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001001/044001001005/MoreInfo.aspx?CategoryNum=044001001005",
         ["name", "ggstart_time", "href"]],


        ["gcjs_kancha_zhongbiao_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001002/044001002001/MoreInfo.aspx?CategoryNum=044001002001",
         ["name", "ggstart_time", "href"]],
        ["gcjs_jianli_zhongbiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001002/044001002002/MoreInfo.aspx?CategoryNum=044001002002",
         ["name", "ggstart_time", "href"]],
        ["gcjs_shigong_zhongbiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001002/044001002003/MoreInfo.aspx?CategoryNum=044001002003",
         ["name", "ggstart_time", "href"]],
        ["gcjs_huowu_zhongbiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001002/044001002004/MoreInfo.aspx?CategoryNum=044001002004",
         ["name", "ggstart_time", "href"]],
        ["gcjs_qita_zhongbiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001002/044001002005/MoreInfo.aspx?CategoryNum=044001002005",
         ["name", "ggstart_time", "href"]],



        ["gcjs_jianli_biangeng_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001003/044001003002/MoreInfo.aspx?CategoryNum=044001003002",
         ["name", "ggstart_time", "href"]],
        ["gcjs_shigong_biangeng_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001003/044001003003/MoreInfo.aspx?CategoryNum=044001003003",
         ["name", "ggstart_time", "href"]],
        ["gcjs_huowu_biangeng_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/044001003/044001003004/MoreInfo.aspx?CategoryNum=044001003004",
         ["name", "ggstart_time", "href"]],



        # ["zfcg_zhaobiao_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044002/044002001/",
        #  ["name", "ggstart_time", "href"]],
        #
        #
        # ["zfcg_biangeng_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044002/044002002/",
        #  ["name", "ggstart_time", "href"]],
        #
        #
        # ["zfcg_zhongbiao_gg","http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044002/044002003/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["ylcg_zhaobiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044004/044004001/MoreInfo.aspx?CategoryNum=044004001",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["ylcg_biangeng_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044004/044004003/MoreInfo.aspx?CategoryNum=044004003",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["ylcg_zhongbiao_gg", "http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044004/044004002/MoreInfo.aspx?CategoryNum=044004002",
        #  ["name", "ggstart_time", "href"]],




    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","laiwu"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044002/044002002/"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 2):
    #     df=f1(driver, 7)
    #     print(df)
