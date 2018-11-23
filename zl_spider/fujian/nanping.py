
import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

import json
from zhulong.util.etl import add_info, est_meta, est_html, est_tbs, gg_existed

_name_="nanping"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    url = driver.current_url
    if "/jsgc/" in url:
        locator = (By.XPATH, "//tr[@class='trfont'][1]/td/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            cnum = re.findall(r'(\d+)/', str)[0]
        except:
            cnum = 1

        if num != int(cnum):
            if "Paging" not in url:
                s = "?Paging=%d" % (num) if num > 1 else "?Paging=1"
                url = url + s
            elif num == 1:
                url = re.sub("Paging=[0-9]*", "Paging=1", url)
            else:
                s = "Paging=%d" % (num) if num > 1 else "Paging=1"
                url = re.sub("Paging=[0-9]*", s, url)
                # print(cnum)
            driver.get(url)

            try:
                locator = (By.XPATH, "//tr[@class='trfont'][1]/td/a[string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (By.XPATH, "//tr[@class='trfont'][1]/td/a[string()!='%s']" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        table = soup.find("table", cellspacing="3")

        trs = table.find_all("tr", class_='trfont')
        data = []
        for tr in trs:
            a = tr.find('a')

            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()

            try:
                link = a["href"]
            except:
                link = ''

            td = tr.find("td", align="right").text.strip()
            td = re.findall(r'\[(.*)\]', td)[0]

            link = "http://npggzy.gov.cn"+link.strip()

            tmp = [title, td, link]
            data.append(tmp)


        df = pd.DataFrame(data)
        df['info'] = None
        return df

    else:
        locator = (By.XPATH, "//li[@class='content-item'][1]/a/span[1]")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            cnum = re.findall(r'(\d+)/', str)[0]
        except:
            cnum = 1

        if num != int(cnum):
            driver.find_element_by_xpath('//input[@id="GoToPagingNo"]').clear()
            driver.find_element_by_xpath('//input[@id="GoToPagingNo"]').send_keys(num)
            driver.find_element_by_xpath('//a[@class="wb-page-item wb-page-next wb-page-go wb-page-fs12"]').click()

            try:
                locator = (By.XPATH, "//li[@class='content-item'][1]/a/span[1][string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (By.XPATH, "//li[@class='content-item'][1]/a/span[1][string()!='%s']" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        table = soup.find("ul", class_="content-list clearfix")

        trs = table.find_all("li", class_='content-item')
        data = []
        for tr in trs:
            a = tr.find('a')

            try:
                title = tr.find('span', class_='link-content').text.strip()
            except:
                title = a.text.strip()

            try:
                link = a["href"]
            except:
                link = ''

            td = tr.find("span", class_="time").text.strip()

            link = "http://npggzy.gov.cn" + link.strip()

            tmp = [title, td, link]
            data.append(tmp)


        df = pd.DataFrame(data)
        df['info'] = None
        return df





def f2(driver):
    url = driver.current_url
    if "/jsgc/" in url:
        locator = (By.XPATH, "//tr[@class='trfont'][1]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            num = re.findall(r'/(\d+)', str)[0]
        except:
            num = 1

        driver.quit()
        return int(num)
    else:
        locator = (By.XPATH, "//li[@class='content-item'][1]/a/span[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            locator = (By.XPATH, "//a[@class='wb-page-default wb-page-number wb-page-family']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            num = re.findall(r'/(\d+)', str)[0]
        except:
            num = 1

        driver.quit()
        return int(num)



def f3(driver, url):
    driver.get(url)
    if "categoryNum=01000" in url:
        categoryNum = int(url[-1])
        locator = (By.CLASS_NAME, "menub6_1")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i = 0
        while before != after:
            before = len(driver.page_source)
            time.sleep(0.1)
            after = len(driver.page_source)
            i += 1
            if i > 5: break

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find('div', id="menutab_6_{}".format(categoryNum))

        div = div.find('td', style="line-height: 25px; color: #4e4e4e; text-align:left;")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    else:

        locator = (By.CLASS_NAME, "main-subcontent")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i = 0
        while before != after:
            before = len(driver.page_source)
            time.sleep(0.1)
            after = len(driver.page_source)
            i += 1
            if i > 5: break

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find('div', class_="article-block")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://npggzy.gov.cn/npztb/jsgc/010001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://npggzy.gov.cn/npztb/jsgc/010002/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["gcjs_zhongbiaohxliubiao_gg",
     "http://npggzy.gov.cn/npztb/jsgc/010004/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://npggzy.gov.cn/npztb/jsgc/010005/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://npggzy.gov.cn/npztb/zfjzcg/009001/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://npggzy.gov.cn/npztb/zfjzcg/009002/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiaoliubiao_gg",
     "http://npggzy.gov.cn/npztb/zfjzcg/009003/",
    ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://npggzy.gov.cn/npztb/zfjzcg/009004/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://npggzy.gov.cn/npztb/qxzbxx/013001/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["qsydw_gg",
     "http://npggzy.gov.cn/npztb/qxzbxx/013002/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["qsydw_zhongbiaohxliubiao_gg",
     "http://npggzy.gov.cn/npztb/qxzbxx/013004/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

    ["qsydw_zhongbiaoliubiao_gg",
     "http://npggzy.gov.cn/npztb/qxzbxx/013004/",
     ["name", "ggstart_time", "href", "info"],f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省南平市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","nanping"])

    # driver=webdriver.Chrome()
    # url = "http://npggzy.gov.cn/npztb/zfjzcg/009003/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)