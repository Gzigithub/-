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

from zhulong.util.etl import est_html,est_meta


_name_='rushan'


def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '//*[@id="1912"]/div/table[1]/tbody/tr/td[2]/span/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("pageNum=(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("pageNum=[0-9]*", "pageNum=1", url)
        else:
            s = "pageNum=%d" % (num) if num > 1 else "pageNum=1"
            url = re.sub("pageNum=[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        try:
            locator = (By.XPATH, "//*[@id='1912']/div/table[1]/tbody/tr/td[2]/span/a[string()='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(4)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="default_pgContainer")
    trs = ul.find_all("table")
    data = []
    for li in trs:

        a = li.find("a")
        title = a['title']
        link = "http://ggzy.rushan.gov.cn" + a["href"]
        try:
            span1 = li.find("span", class_="bt_time").text
        except:
            span1 = ""

        tmp = [title.strip(), span1.strip(), link]
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
    locator = (By.XPATH, '//*[@id="1912"]/div/table[1]/tbody/tr/td[2]/span/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@class='default_pgTotalPage']")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = page_all.strip()
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)

def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"xxlb")

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

    div=soup.find('div',class_='xxlb')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div



data = [
        ["gcjs_zhaobiao_gg","http://ggzy.rushan.gov.cn/col/col1823/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_biangeng_gg", "http://ggzy.rushan.gov.cn/col/col1824/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zhongbiao_gg", "http://ggzy.rushan.gov.cn/col/col1825/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],


        ["zfcg_biangeng_gg", "http://ggzy.rushan.gov.cn/col/col1827/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhaobiao_gg", "http://ggzy.rushan.gov.cn/col/col1826/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhongbiao_gg", "http://ggzy.rushan.gov.cn/col/col1828/index.html?uid=1912&pageNum=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]


def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省乳山市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","rushan"])