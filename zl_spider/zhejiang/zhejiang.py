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


_name_="zhejiang"



# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver, num):
    locator = (By.XPATH, "//table[@width='98%']/tbody/tr[1]/td/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//td[@class='huifont']")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]
    url = driver.current_url
    if num != int(cnum):
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)

        try:
            locator = (By.XPATH, "//table[@width='98%']/tbody/tr[1]/td/a[string()!='{}']".format(val))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//table[@width='98%']/tbody/tr[1]/td/a[string()!='{}']".format(val))
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table= soup.find("table", width='98%')

    tbody = table.find("tbody")

    trs = tbody.find_all("tr", height="30")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            continue
        tds = tr.find("td", width="80").text
        td = re.findall(r"\[(.*)\]", tds)[0]
        tmp = [a["title"].strip(), td.strip(), "http://new.zmctc.com"+link.strip()]

        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//table[@width='98%']/tbody/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//td[@class='huifont']")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "bg2")

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

    div = soup.find('td', class_='border')
    div=div.find_all('tr')[1]

    return div


data = [
    ["zhaobiao_gongcheng_gg","http://new.zmctc.com/zjgcjy/jyxx/004001/004001001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhaobiao_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004001/004001002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhaobiao_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004001/004001003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["biangeng_gongcheng_gg", "http://new.zmctc.com/zjgcjy/jyxx/004002/004002001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["biangeng_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004002/004002002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["biangeng_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004002/004002003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["dengji_gongcheng_gg", "http://new.zmctc.com/zjgcjy/jyxx/004003/004003001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["dengji_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004003/004003002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["dengji_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004003/004003003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zishenjieguo_gongcheng_gg", "http://new.zmctc.com/zjgcjy/jyxx/004004/004004001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zishenjieguo_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004004/004004002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zishenjieguo_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004004/004004003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiaohx_gongcheng_gg", "http://new.zmctc.com/zjgcjy/jyxx/004006/004006001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiaohx_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004006/004006002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiaohx_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004006/004006003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiao_gongcheng_gg", "http://new.zmctc.com/zjgcjy/jyxx/004010/004010001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiao_huowu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004010/004010002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiao_fuwu_gg", "http://new.zmctc.com/zjgcjy/jyxx/004010/004010003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省省级",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","zhejiang"])


    # driver=webdriver.Chrome()
    # url="http://new.zmctc.com/zjgcjy/jyxx/004001/004001001/?Paging=1"
    # driver.get(url)
    # # df = f3(driver, url)
    # # print(df)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 5):
    #     df=f1(driver, i)
    #     print(df)