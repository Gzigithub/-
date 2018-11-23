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

_name_='rongcheng'

def f1(driver, num):
    locator = (By.XPATH, '//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b')
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    if num != int(cnum):
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        # time.sleep(0.5)

        try:
            locator = (By.XPATH, "//*[@id='MoreInfoList1_Pager']/table/tbody/tr/td[1]/font[3]/b[string()='%s']" % num)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(3)

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("table", id="MoreInfoList1_DataGrid1")

    trs = tbody.find_all("tr")
    data = []
    for tr in trs:
        a = tr.find("a")
        title = a['title']

        td = tr.find_all("td")
        span_1 = td[2].text.strip()
        # print(span_1)

        tmp = [title.strip(), span_1,"http://www.rcggzy.cn" + a["href"]]
        data.append(tmp)
        # print(tmp)

    df = pd.DataFrame(data=data)
    df["info"]=None
    return df




def f2(driver):

    locator = (By.XPATH, '//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[2]/b')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = page_all.strip()

    driver.quit()

    return int(page)



def f3(driver,url):


    driver.get(url)

    locator=(By.ID,"tblInfo")

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

    div=soup.find('table',id='tblInfo')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div



data = [
        ["gcjs_zhaobiao_gg","http://www.rcggzy.cn/rcweb/004/004001/004001001/MoreInfo.aspx?CategoryNum=004001001",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zuigaoxianjia_gg", "http://www.rcggzy.cn/rcweb/004/004001/004001002/MoreInfo.aspx?CategoryNum=004001002",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zhongbiao_gg","http://www.rcggzy.cn/rcweb/004/004001/004001003/MoreInfo.aspx?CategoryNum=004001003",
         ["name", "ggstart_time", "href","info"],f1,f2],


        ["zfcg_zhaobiao_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004001/MoreInfo.aspx?CategoryNum=004002004001",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_biangeng_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004002/MoreInfo.aspx?CategoryNum=004002004002",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhongbiao_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002004/004002004003/MoreInfo.aspx?CategoryNum=004002004003",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_xuqiu_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005001/MoreInfo.aspx?CategoryNum=004002005001",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_hetong_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005002/MoreInfo.aspx?CategoryNum=004002005002",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_hetong_gg",
         "http://www.rcggzy.cn/rcweb/004/004002/004002005/004002005003/MoreInfo.aspx?CategoryNum=004002005003",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qsydw_zhaobiao_gg", "http://www.rcggzy.cn/rcweb/004/004006/004006001/MoreInfo.aspx?CategoryNum=004006001",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qsydw_zhongbiao_gg", "http://www.rcggzy.cn/rcweb/004/004006/004006003/MoreInfo.aspx?CategoryNum=004006003",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qita_zhaobiao_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004001/MoreInfo.aspx?CategoryNum=004004001",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qita_biangeng_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004002/MoreInfo.aspx?CategoryNum=004004002",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qita_zhongbiao_gg", "http://www.rcggzy.cn/rcweb/004/004004/004004003/MoreInfo.aspx?CategoryNum=004004003",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]


def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省荣成市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","rongcheng"])