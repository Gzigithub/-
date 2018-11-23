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

from zhulong.util.etl import est_tables,gg_html,gg_meta,est_html


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]

_name_='qingdao'



def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//td[@class="box_td"]/a)[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("pageIndex=(.*)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("pageIndex=[0-9]*", "pageIndex=1", url)
        else:
            s = "pageIndex=%d" % (num) if num > 1 else "pageIndex=1"
            url = re.sub("pageIndex=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//td[@class='box_td']/a)[1]").text
        # print(url)
        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, "(//td[@class='box_td']/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        # print("22222")

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="info_con")
    trs = ul.find_all("tr")
    data = []
    for li in trs:
        td = li.find("td", class_="box_td")
        a = td.find("a")
        link = "http://202.110.193.29:10000" + a["href"]

        span2 = li.find_all("td")[1]

        tmp = [a.text.strip(), span2.text.strip(), link]
        data.append(tmp)
        # print(data)
    df = pd.DataFrame(data=data)
    df["info"]=None
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    locator = (By.XPATH, '(//td[@class="box_td"]/a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//div[@class="pages"]/a[last()]')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        url = driver.current_url
        # print(url)
        page = int(re.findall("pageIndex=(.*)", url)[0])
        # page = re.findall('/(.*)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    driver.quit()
    return int(page)


def f3(driver,url):


    driver.get(url)
    try:
        locator=(By.ID,"htmlTable")

        WebDriverWait(driver,5).until(EC.presence_of_all_elements_located(locator))
    except:
        locator=(By.CLASS_NAME,"detail")

        WebDriverWait(driver,5).until(EC.presence_of_all_elements_located(locator))
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

    if "htmlTable" in page:
        div=soup.find('div',id='htmlTable')
    else:

        div=soup.find('div',class_='detail')
    
    return div


data = [
        ["gcjs_zhaobiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-0?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_zigeshencha_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-4?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_yuzhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-2?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_feibiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-3?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_zhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-8?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_jiaoyijincheng_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/0-0-9?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhaobiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-0?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        # ["zfcg_biangeng_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-5?pageIndex=1",
        #  ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhongbiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-2?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_feibiao_gg", "http://202.110.193.29:10000/Tradeinfo-GGGSList/1-1-3?pageIndex=1",
         ["name", "ggstart_time", "href","info"],f1,f2],
    ]






#est_tables(conp=["postgres","since2015","192.168.3.172","shandong","qingdao"],data=data[-2:])

def work(conp,**args):
    gg_meta(conp,data=data,diqu="山东省青岛市",**args)
    gg_html(conp,f=f3,**args)

if __name__=='__main__':

    work(conp=["postgres","since2015","127.0.0.1","shandong","qingdao"])

#est_html(conp=["postgres","since2015","127.0.0.1","shandong","qingdao"],f=f3,num=10)


