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

from zhulong.util.etl import est_tables,gg_meta,gg_html,est_meta,est_html


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]
_name_='weihai'




def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//ul[@class="article-list2"]/li/div/a)[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "index.jhtml" in url:
        url = re.sub("index", "index_1", url)
        driver.get(url)
    cnum = int(re.findall("index_(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)
            # print(cnum)
        # print(url)
        driver.get(url)
        locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(' (\d+)/', page_all)[0]
        if int(page) != num:
            time.sleep(5)


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("ul", class_="article-list2")
    trs = ul.find_all("li")
    data = []
    for li in trs:

        a = li.find("a")
        link = "http://www.whggzyjy.cn" + a["href"]
        try:
            span1 = li.find_all("div", class_="list-times")[0].text
        except:
            span1 = ""

        tmp = [a.text.strip(), span1.strip(), link]
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
    locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "(//ul[@class='pages-list']/li)[1]")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = re.findall('/(\d+)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)


def f3(driver,url):


    driver.get(url)

    locator=(By.ID,"content")

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

    div=soup.find('div',id='content')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div




data = [
        ["gcjs_zhaobiao_gg","http://www.whggzyjy.cn/jyxxzbxm/index.jhtml",["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zigeshencha_gg", "http://www.whggzyjy.cn/jyxxzbgg/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_kaibiaojilu_gg", "http://www.whggzyjy.cn/jyxxkbjl/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zhongbiao_gg", "http://www.whggzyjy.cn/jyxxzbgs/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zbwenjianchengqin_gg", "http://www.whggzyjy.cn/jyxxzbwj/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_yucai_gg", "http://www.whggzyjy.cn/jyxxcgxq/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhaobiao_gg", "http://www.whggzyjy.cn/jyxxcggg/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhongbiao_gg", "http://www.whggzyjy.cn/jyxxcjgg/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_hetong_gg", "http://www.whggzyjy.cn/jyxxcght/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_yanshou_gg", "http://www.whggzyjy.cn/jyxxysbg/index.jhtml", ["name", "ggstart_time", "href","info"],f1,f2],

    ]


def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省威海市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","weihai"])

# driver=webdriver.Chrome()
# url="http://www.whggzyjy.cn/jyxxzbgg/7374.jhtml "

# driver.get(url)

