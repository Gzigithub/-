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

import json 

from zhulong.util.etl import est_tables,gg_meta,gg_html,est_meta,est_html


_name_='weifang'


def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//span[@class="info-name"])[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("Paging=(.*)", url)[0])
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
        link = "http://ggzy.weifang.gov.cn" + a["href"]
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
        except:
            state = ""
        tmp = [info_number.strip(), a.text.strip(), span1.strip(), span2.strip(), link]#, state.strip()]
        data.append(tmp)
    df = pd.DataFrame(data=data)
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
        # print(url)
        page = re.findall('/(.*)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)

def add_info(f,info):
    def wrap(*arg):
        df=f(*arg)
        df["info"]=json.dumps(info,ensure_ascii=False)
        return df 
    return wrap

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
        "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012001&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["gcjs_biangeng_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012002&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["gcjs_dayi_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012005&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href","info"],f1,f2],
        ["gcjs_zhongbiaohx_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012006&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href","info"],f1,f2],
        ["gcjs_zhongbiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012007&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["gcjs_liubiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_ggycgg.aspx?address=&type=&categorynum=004012010&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        
        ["gcjs_danyilaiyuan_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg.aspx?address=&type=&categorynum=004012008&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],


        ["zfcg_zhaobiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg_cgxq.aspx?address=&categorynum=004002017&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_zhongbiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcgtwo.aspx?address=&type=&categorynum=004002001&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_biangeng_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002011&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_zhongbiaoshencha_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002012&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_liubiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002016&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_zhongzhi_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002015&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        
        ["zfcg_yanshou_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002014&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["zfcg_caigouhetong_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_zfcg.aspx?address=&type=&categorynum=004002013&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        
        ["ylsb_zhaobiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006001&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["ylsb_biangeng_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006002&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["ylsb_zhongbiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006003&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["ylsb_yanshou_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006007&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["ylsb_liubiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004006008&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

        ["qsydw_zhaobiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007001&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["qsydw_biangeng_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007004&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["qsydw_zhongbiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007002&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href","info"],f1,f2],
        ["qsydw_zhongzhi_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007007&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],
        ["qsydw_liubiao_gg",
         "http://ggzy.weifang.gov.cn/wfggzy/showinfo/moreinfo_gg_ylsb.aspx?address=&categorynum=004007009&Paging=1",
         ["info_number", "name", "ggstart_time", "ggend_time", "href", "info"],f1,f2],

    ]


#est_tables(conp=["postgres","since2015","192.168.3.172","shandong","weifang"],data=data)


def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省潍坊市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","weifang"])

