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
    if "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/" in url:
        print("111")
        if "CategoryNum" in url:
            # url_1 = url.rsplit('/', maxsplit=3)[0]
            driver.get("http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/")
        driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(num)).click()
        locator = (By.XPATH, "(//table[@cellspacing='2']/tbody/tr[1]/td/a)[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        html = driver.page_source
        html_data = etree.HTML(html)
        page = html_data.xpath('(//font[@class="MoreinfoColor"])/text()')
        n = len(page)
        data_list = []
        for j in range(int(n) + 1):
            if j == 0:
                continue
            else:
                url_2 = driver.current_url
                if "CategoryNum" in url_2:
                    # print(url)
                    # url_3 = url_2.rsplit('/', maxsplit=2)[0]
                    # print(url_3)
                    driver.get("http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/002005001001/")
                driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(j)).click()
                locator = (By.XPATH, "(//tr[@class='TDStylemore']/td/a)[1]")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                html = driver.page_source
                if "更多信息" in html:
                    driver.find_element_by_xpath("//td[@align='right' and @valign='bottom']/a").click()
                    locator = (By.XPATH, "//*[@id='MoreInfoList1_DataGrid1']/tbody/tr[1]/td[2]/a")
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                    try:
                        html = driver.page_source
                        html_data = etree.HTML(html)
                        page_all = html_data.xpath('//*[@id="MoreInfoList1_Pager"]/a[last()]/@title')[0]
                        print(page_all)
                        page = re.findall(r"(\d+)", page_all)[0]
                    except:
                        page = 1
                    # 获取总页数
                    print(page)
                    for i in range(int(page) + 1):
                        if i == 0:
                            continue
                        else:
                            # print(i)
                            df = f1_data(driver, i)
                            # print(df)
                            data_list.append(df)

        data = []
        for i in data_list:
            for j in i:
                data.append(j)

        df = pd.DataFrame(data=data)
        # print(df)
        return df


    else:
        if "CategoryNum" in url:
            url_1 = url.rsplit('/', maxsplit=2)[0]
            driver.get(url_1)

        locator = (By.XPATH, "(//table[@cellspacing='2']/tbody/tr[1]/td/a)[{}]".format(num))
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(val)
        href = driver.find_element_by_xpath('(//font[@class="MoreinfoColor"])[{}]'.format(num)).click()
        # link = "http://www.dyggzyjy.gov.cn" + href
        # driver.get(link)
        locator = (By.XPATH, "(//tr[@class='TDStylemore']/td/a)[1]")
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
            tal = driver.find_element_by_xpath("(//tr[@class='TDStylemore']/td/a)[1]").text
            driver.find_element_by_xpath("//td[@align='right' and @valign='bottom']/a").click()

            locator = (By.XPATH, "//*[@id='MoreInfoList1_DataGrid1']/tbody/tr[1]/td[2]/a")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            try:
                page_all = driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/a[last()]').text
                page = re.findall(r"(\d+)", page_all)[0]
            except:
                page = 1
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
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/font').text)
    except Exception as e:
        cnum = 1
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
    # print(cnum)
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
            tmp = [a["title"], td.text.strip(), "http://www.bzggzyjy.gov.cn" + a["href"]]
            data.append(tmp)
        except:
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
        ["gcjs_zhaobiao_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004001/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_zhongbiao_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004002/",
         ["name", "ggstart_time", "href"]],


        ["gcjs_biangeng_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002004/002004003/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_zhaobiao_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_biangeng_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005002/",
         ["name", "ggstart_time", "href"]],


        ["zfcg_zhongbiao_gg","http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005003/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_yucai_gg", "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005004/",
         ["name", "ggstart_time", "href"]],
        #
        # ["zfcg_hetong_gg", "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005005/",
        #  ["name", "ggstart_time", "href"]],

        ["zfcg_yanshou_gg", "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005006/",
         ["name", "ggstart_time", "href"]],

        ["zfcg_liubiao_gg", "http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005007/",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","bingzhou"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.bzggzyjy.gov.cn/bzweb/002/002005/002005001/"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 5):
    #     df=f1(driver, i)
    #     print(df)
