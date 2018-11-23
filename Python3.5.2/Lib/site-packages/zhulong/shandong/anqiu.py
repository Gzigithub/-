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

from zhulong.util.etl import est_tbs,est_gg,est_cdc,est_meta,est_html_work,est_html_cdc,est_html

_name_='anqiu'

def f1(driver, num):

    locator = (By.XPATH, '(//span[@class="info-name"])[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("Paging=(\d+)", url)[0])
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
        link = "http://aqggzy.weifang.gov.cn" + a["href"]
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
            state = re.findall(r'\[(.*)\]', state)[0]
        except:
            state = ""
        tmp = [info_number.strip(), a.text.strip(), span1.strip(), span2.strip(), link, state.strip()]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    del df[df.columns[-1]]
    df["info"]=None
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
        page = re.findall(r'/(\d+)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)

def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"detail-content")

    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located(locator))

    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source

    soup=BeautifulSoup(page,'lxml')

    div=soup.find('div',class_='detail-content')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div


data = [
    ["gcjs_zhaobiao_gg",
    "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg.aspx?type=&categorynum=004012001&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg.aspx?type=&categorynum=004012006&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg.aspx?type=&categorynum=004012007&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],


    ["zfcg_yucai_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcg_cgxq.aspx?categorynum=004002017&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?categorynum=004002001&type=&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["zfcg_biangeng_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcg.aspx?categorynum=004002011&type=&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcg.aspx?categorynum=004002012&type=&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["zfcg_liubiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcg.aspx?categorynum=004002016&type=&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],


    ["zfcg_yanshou_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_zfcg.aspx?type=&categorynum=004002014&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],


    ["ylcg_zhaobiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_ylsb.aspx?categorynum=004006001&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["ylcg_zhongbiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_ylsb.aspx?categorynum=004006003&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["ylcg_liubiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_ylsb.aspx?categorynum=004006008&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["jqita_zhaobiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_qt.aspx?categorynum=004007001&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["jqita_biangeng_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_qt.aspx?categorynum=004007004&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["jqita_zhongbiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_qt.aspx?categorynum=004007002&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ["jqita_liubiao_gg",
     "http://aqggzy.weifang.gov.cn/anqggzy/showinfo/moreinfo_gg_qt.aspx?categorynum=004007009&Paging=1",
     ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

]





def work(conp,**args):
    est_meta(conp=conp,data=data,diqu="山东省安丘市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    work(conp=["postgres","since2015","127.0.0.1","shandong","anqiu"])