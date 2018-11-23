
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
from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="zhuji"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)







def f1(driver, num):
    url = driver.current_url
    if "showinfo/MoreinfoFZX_TZGG.aspx" in url:
        locator = (By.XPATH, "//table[@id='sl2_DataGrid1']/tbody/tr[1]/td/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
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

            locator = (By.XPATH, "//table[@id='sl2_DataGrid1']/tbody/tr[1]/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find("table", id="sl2_DataGrid1")
        trs = table.find_all("tr", valign="top")
        data = []
        for tr in trs:
            a = tr.find("a")
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"]
            except:
                link = ''
            try:
                td = tr.find("td", align="right").text.strip()
            except:
                td = tr.find_all("td", align="center")[1].text.strip()

            link = "http://www.zjztb.gov.cn" + link.strip()

            tmp = [title, td, link]
            data.append(tmp)

        df = pd.DataFrame(data)
        df['info'] = None
        return df

    else:
        locator = (By.XPATH, "//tr[@height='26'][1]/td/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
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

            locator = (By.XPATH, "//tr[@height='26'][1]/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        table = soup.find("table", cellspacing="3")

        trs = table.find_all("tr", height="26")
        data = []
        for tr in trs:
            a = tr.find("a")
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"]
            except:
                link = ''
            try:
                td = tr.find("td", align="right").text.strip()
            except:
                td = tr.find_all("td", align="center")[1].text.strip()

            link = "http://www.zjztb.gov.cn"+link.strip()
            tmp = [title, td, link]
            data.append(tmp)
        df = pd.DataFrame(data)
        df['info'] = None
        return df


def f2(driver):

    url = driver.current_url
    if "showinfo/MoreinfoFZX_TZGG.aspx" in url:
        locator = (By.XPATH, "//table[@id='sl2_DataGrid1']/tbody/tr[1]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    else:
        locator = (By.XPATH, "//tr[@height='26'][1]/td/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(re.findall(r'/(\d+)', str)[0])
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "container")
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
    time.sleep(1)
    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find('div', class_="positive-content")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.zjztb.gov.cn/TPFront/jsgc/026002/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.zjztb.gov.cn/TPFront/jsgc/026003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://www.zjztb.gov.cn/TPFront/jsgc/026004/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://www.zjztb.gov.cn/TPFront/zfcg/020002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://www.zjztb.gov.cn/TPFront/zfcg/020003/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiaohx_gg",
     "http://www.zjztb.gov.cn/TPFront/zfcg/020004/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.zjztb.gov.cn/TPFront/zfcg/020005/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_yucai_gg",
     "http://www.zjztb.gov.cn/TPFront/ggdf/037001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhaobiao_gg",
     "http://www.zjztb.gov.cn/TPFront/ggdf/037002/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiaohx_gg",
     "http://www.zjztb.gov.cn/TPFront/ggdf/037003/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://www.zjztb.gov.cn/TPFront/ggdf/037004/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_tongzhi_gg",
     "http://www.zjztb.gov.cn/TPFront/showinfo/MoreinfoFZX_TZGG.aspx?type=001&categorynum=028&Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_gg",
     "http://www.zjztb.gov.cn/TPFront/showinfo/MoreinfoFZX_TZGG.aspx?type=002&categorynum=028&Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiaohx_gg",
     "http://www.zjztb.gov.cn/tpfront/showinfo/MoreinfoFZX_TZGG.aspx?type=003&categorynum=028&Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_gg",
     "http://www.zjztb.gov.cn/TPFront/showinfo/MoreinfoFZX_TZGG.aspx?type=004&categorynum=028&Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]



def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省诸暨市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","zhuji"])

    # driver=webdriver.Chrome()
    # url="http://www.zjztb.gov.cn/TPFront/showinfo/MoreinfoFZX_TZGG.aspx?type=004&categorynum=028&Paging=1"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    #
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
