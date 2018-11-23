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

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs

from collections import OrderedDict


_name_='laiwu'


def f1(driver, num):
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text.strip())
    except StaleElementReferenceException:
        cnum = int(driver.find_element_by_xpath('//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[1]/font[3]/b').text.strip())
    val = driver.find_element_by_xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr[1]/td[2]/a').text
    if num != cnum:
        driver.execute_script("javascript:__doPostBack('MoreInfoList1$Pager','{}')".format(num))
        time.sleep(0.5)
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
            tmp = [a.text.strip(), td.text.strip(), "http://ggzy.laiwu.gov.cn" + a["href"]]
            data.append(tmp)
        except:
            a = tr.find_all("td")[1]
            td = tr.find_all("td")[2]
            tmp = [a.text.strip(), td.text.strip(), ""]
            data.append(tmp)
    df=pd.DataFrame(data=data)
            # print(tmp)
    df["info"]=None


    return df

def f2(driver):
    try:
        locator = (By.ID, 'MoreInfoList1_Pager')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        txt=driver.find_element_by_id("MoreInfoList1_Pager").text
        total=int(re.findall("总页数：([0-9]*)",txt)[0])
        if total==0:
            time.sleep(1)
            txt=driver.find_element_by_id("MoreInfoList1_Pager").text
            total=int(re.findall("总页数：([0-9]*)",txt)[0])
    except:
        
        total=1
    driver.quit()
    return total


def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"infodetail")

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

    div=soup.find('td',class_='infodetail')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div

def get_data():
    gctype=OrderedDict([("勘察设计","001"),("监理","002"),("施工","003"),("货物","004"),("其它","005")])
    ggtype=OrderedDict([("zhaobiao","001"),("zhongbiao","002"),("biangeng","003")])
    xs=OrderedDict([("市本级","001"),("莱城区","002"),("钢城区","003"),("高新区","004"),("雪野旅游区","005"),("经济开发区","006"),("其它","007")])
    ggtype2=OrderedDict([("zhaobiao","001"),("zhongbiao","003"),("biangeng","002")])
    data=[]
    for w1 in ggtype.keys():
        for w2 in gctype.keys():
            p1="044001%s"%(ggtype[w1])
            p2="044001%s%s"%(ggtype[w1],gctype[w2])
            href="http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044001/%s/%s/MoreInfo.aspx?CategoryNum=%s"%(p1,p2,p2)
            tmp=["gcjs_%s_gctype%s_gg"%(w1,gctype[w2]),href,["name","ggstart_time","href","info"],add_info(f1,{"gctype":w2}),f2]
            data.append(tmp)


    for w1 in ggtype2.keys():
        for w2 in xs.keys():
            p1="044002%s"%(ggtype2[w1])
            p2="044002%s%s"%(ggtype2[w1],xs[w2])
            href="http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044002/%s/%s/MoreInfo.aspx?CategoryNum=%s"%(p1,p2,p2)
            tmp=["zfcg_%s_xs%s_gg"%(w1,xs[w2]),href,["name","ggstart_time","href","info"],add_info(f1,{"diqu":w2}),f2]
            data.append(tmp)

    for w1 in ggtype.keys():
            p1="044004%s"%(ggtype2[w1])

            href="http://ggzy.laiwu.gov.cn/lwwznew/jyxx/044004/%s/MoreInfo.aspx?CategoryNum=%s"%(p1,p1)
            tmp=["yiliao_%s_gg"%w1,href,["name","ggstart_time","href","info"],f1,f2]
            data.append(tmp)

    remove_arr=["gcjs_biangeng_gctype004_gg","gcjs_biangeng_gctype005_gg","gcjs_biangeng_gctype005_gg"]
    data1=data.copy()
    for w in data:
        if w[0] in remove_arr:data1.remove(w)
    return data1

data=get_data()







def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省莱芜市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","laiwu"])

#est_tbs(conp=["postgres","since2015","127.0.0.1","shandong","laiwu"],data=data[-8:],total=1,num=1)
