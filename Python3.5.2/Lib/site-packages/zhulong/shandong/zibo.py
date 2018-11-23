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

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs

from collections import OrderedDict

_name_='zibo'

def f1(driver, num):
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/div[1]/font[3]/b').text)
    except Exception as e:
        cnum = 1
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text

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
            tmp = [a["title"].strip(), td.text.strip(), "http://ggzyjy.zibo.gov.cn" + a["href"]]
            data.append(tmp)
        except:
            print("error_data")
            a = tr.find_all("td")[1]
            td = tr.find_all("td")[2]
            tmp = [a.text.strip(), td.text.strip(), ""]
            data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None

    return df




def f2(driver):
    try:
        locator = (By.ID, 'MoreInfoList1_Pager')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        txt=driver.find_element_by_id("MoreInfoList1_Pager").text
        total=int(re.findall("总页数：([0-9]*)",txt)[0])
    except:
        total=1
    driver.quit()
    return total


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

def get_data():
    data=[]
    ggtype1=OrderedDict([("zhaobiao","001"),("biangeng","002"),("zhongbiaohx","003")])

    sx=OrderedDict([("市本级","001"),("张店区","002"),("高新区","003"),("文昌湖区","004"),("高青县","005"),("临淄区","006"),("桓台县","007"),("博山区","008")])

    hrefs=[
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001001/MoreInfo.aspx?CategoryNum=268698113",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001002/MoreInfo.aspx?CategoryNum=268698114",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001004/MoreInfo.aspx?CategoryNum=268698116",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001005/MoreInfo.aspx?CategoryNum=268698117",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001006/MoreInfo.aspx?CategoryNum=268698118",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001007/MoreInfo.aspx?CategoryNum=268698119",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001008/MoreInfo.aspx?CategoryNum=2001001008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001001/002001001009/MoreInfo.aspx?CategoryNum=2001001009",#shanchu

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002001/MoreInfo.aspx?CategoryNum=268698625",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002002/MoreInfo.aspx?CategoryNum=268698626",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002004/MoreInfo.aspx?CategoryNum=268698628",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002005/MoreInfo.aspx?CategoryNum=268698629",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002006/MoreInfo.aspx?CategoryNum=268698630",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002007/MoreInfo.aspx?CategoryNum=268698631",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002008/MoreInfo.aspx?CategoryNum=2001002008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001002/002001002009/MoreInfo.aspx?CategoryNum=2001002009",#xx

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003001/MoreInfo.aspx?CategoryNum=268699137",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003002/MoreInfo.aspx?CategoryNum=268699138",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003004/MoreInfo.aspx?CategoryNum=268699140",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003005/MoreInfo.aspx?CategoryNum=268699141",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003006/MoreInfo.aspx?CategoryNum=268699142",#xx
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003007/MoreInfo.aspx?CategoryNum=268699143",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003008/MoreInfo.aspx?CategoryNum=2001003008",#xx
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002001/002001003/002001003009/MoreInfo.aspx?CategoryNum=2001003009",

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001001/MoreInfo.aspx?CategoryNum=268960257",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960258",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960260",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960261",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960262",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001002/MoreInfo.aspx?CategoryNum=268960263",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001008/MoreInfo.aspx?CategoryNum=2002001008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001009/MoreInfo.aspx?CategoryNum=2002001009",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002001/002002001010/MoreInfo.aspx?CategoryNum=268960264",

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002001/MoreInfo.aspx?CategoryNum=268960769",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002002/MoreInfo.aspx?CategoryNum=268960770",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002004/MoreInfo.aspx?CategoryNum=268960772",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002007/MoreInfo.aspx?CategoryNum=268960773",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002007/MoreInfo.aspx?CategoryNum=268960774",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002007/MoreInfo.aspx?CategoryNum=268960775",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002008/MoreInfo.aspx?CategoryNum=2002002008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002009/MoreInfo.aspx?CategoryNum=2002002009",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002002/002002002010/MoreInfo.aspx?CategoryNum=268960776",#

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003001/MoreInfo.aspx?CategoryNum=268961281",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003002/MoreInfo.aspx?CategoryNum=268961282",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003004/MoreInfo.aspx?CategoryNum=268961284",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003005/MoreInfo.aspx?CategoryNum=268961285",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003006/MoreInfo.aspx?CategoryNum=268961286",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003007/MoreInfo.aspx?CategoryNum=268961287",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003008/MoreInfo.aspx?CategoryNum=2002003008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003009/MoreInfo.aspx?CategoryNum=2002003009",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002003/002002003010/MoreInfo.aspx?CategoryNum=268961288",

        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004001/MoreInfo.aspx?CategoryNum=268961793",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004002/MoreInfo.aspx?CategoryNum=268961794",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004004/MoreInfo.aspx?CategoryNum=268961796",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004006/MoreInfo.aspx?CategoryNum=268961797",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004006/MoreInfo.aspx?CategoryNum=268961798",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004007/MoreInfo.aspx?CategoryNum=268961799",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004008/MoreInfo.aspx?CategoryNum=2002004008",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004009/MoreInfo.aspx?CategoryNum=2002004009",
        "http://ggzyjy.zibo.gov.cn/TPFront/jyxx/002002/002002004/002002004010/MoreInfo.aspx?CategoryNum=268961800"

        ]
    i=0
    for w1 in ggtype1.keys():
        for w2 in sx.keys():
            href=hrefs[i]
            i+=1
            tmp=["gcjs_%s_diqu%s_gg"%(w1,sx[w2]),href,["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":w2}),f2]
            data.append(tmp)

    ggtype2=OrderedDict([("zhaobiao","001"),("biangeng","002"),("zhongbiaohx","003"),("yucai","004")])
    sx2=OrderedDict([("市本级","001"),("张店区","002"),("高新区","003"),("文昌湖区","004"),("沂源县","005"),("博山区","006"),("高青县","007"),("临淄区","008"),("桓台县","009")])
    for w1 in ggtype2.keys():
        for w2 in sx.keys():

            href=hrefs[i]
            i+=1
            tmp=["zfcg_%s_diqu%s_gg"%(w1,sx[w2]),href,["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":w2}),f2]
            data.append(tmp)
    data1=data.copy()
    arr=["gcjs_zhaobiao_diqu008_gg","gcjs_biangeng_diqu008_gg","gcjs_zhongbiaohx_diqu005_gg","gcjs_zhongbiaohx_diqu007_gg"
    ,"gcjs_zhongbiaohx_diqu008_gg","zfcg_zhongbiaohx_diqu002_gg"]
    for w in data:
        if w[0] in arr:data1.remove(w)
    return data1

data=get_data()


def work(conp,**args):
    #est_meta(conp,data=data,diqu="山东省淄博市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","zibo"])

#est_tbs(conp=["postgres","since2015","127.0.0.1","shandong","zibo"],data=data[30:],total=1,num=1)