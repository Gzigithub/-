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



from zhulong.util.etl import est_tables,gg_meta,gg_html

_name_='jiaozhou'

def f1(driver, num):
    locator = (By.XPATH, "(//li[@class='lnWithData']/a)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    try:
        page_all = driver.find_element_by_xpath('//span[@class="td_Page"]').text
        cnum = re.findall(r'第(\d+)页', page_all)[0]
    except Exception as e:
        page_all = driver.find_element_by_xpath('//span[@class="td_Page"]').text
        cnum = re.findall(r'第(\d+)页', page_all)[0]
    val = driver.find_element_by_xpath('(//li[@class="lnWithData"]/a)[1]').text
    if num != int(cnum):
        driver.execute_script("javascript:pgTo({})".format(num-1))
        # time.sleep(0.5)
        try:
            locator = (By.XPATH, "(//li[@class='lnWithData']/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(1)

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("ul", class_="infoList")

    trs = tbody.find_all("li", class_='lnWithData')
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            stat = tr.find('span').text.strip()
            state = re.findall(r'\[(.*)\]', stat)[0]
        except:
            state = ""
        span_1 = tr.find('span').text.strip()
        span_2 = re.findall(r'(\d+.*)', span_1)[0]

        tmp = [a.text.strip(), span_2, "http://jzggzy.jiaozhou.gov.cn/" + a["href"]]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    df["info"]=None
    # print(df)
    return df




def f2(driver):

    locator = (By.XPATH, '//span[@class="td_Page"]')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = re.findall(r'共(\d+)页', page_all)[0]

    driver.quit()
    return int(page)


def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"gggsTb")

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

    div=soup.find('table',class_='gggsTb')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div





data = [
        ["gcjs_zhaobiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?type=GJGG",
         ["name", "ggstart_time", "href","info"],f1,f2],


        ["gcjs_zhongbiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?regCode=&type=GJGS&subType=0",
         ["name", "ggstart_time", "href","info"],f1,f2],



        ["zfcg_zhaobiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?type=ZCGG",
         ["name",  "ggstart_time", "href","info"],f1,f2],

        ["zfcg_zhongbiao_gg","http://jzggzy.jiaozhou.gov.cn/list.jsp?regCode=&type=ZCGS&subType=0",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]


# url="http://jzggzy.jiaozhou.gov.cn/list.jsp?type=GJGG"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
#est_tables(conp=["postgres","since2015","192.168.3.172","shandong","jiaozhou"],data=data)

def work(conp,**args):
    gg_meta(conp,data=data,diqu="山东省胶州市",**args)
    gg_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","jiaozhou"])