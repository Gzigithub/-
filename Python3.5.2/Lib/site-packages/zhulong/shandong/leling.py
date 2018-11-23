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

_name_='leling'


def f1(driver, num):
    locator = (By.XPATH, "(//a[@class='ewb-list-name'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "Paging=" not in url:
        url = url + "?Paging=1"
        driver.get(url)
        cnum = 1
    else:
        cnum = int(re.findall("Paging=(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//a[@class='ewb-list-name'])[1]").text

        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(r'(\d+)/', page_all)[0]
        if int(page) != num:
            locator = (By.XPATH, "(//a[@class='ewb-list-name'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    tb = soup.find("table", cellspacing="3", align="center")
    trs = tb.find_all("tr")
    data = []
    for li in trs[1:]:
        # print(li)
        a = li.find("a")
        title = a['title']
        # print(a["title"])
        link = "http://ll.dzzyjy.gov.cn" + a["href"]
        span = li.find("font")
        tmp = [title.strip(), span.text.strip(), link]
        data.append(tmp)

        # print(data)
    df = pd.DataFrame(data=data)
    df["info"]=None
    return df




def f2(driver):

    locator = (By.XPATH, '//td[@class="huifont"]')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = re.findall(r'/(\d+)', page_all)[0]

    driver.quit()
    return int(page)

def f3(driver,url):


    driver.get(url)
    time.sleep(1)
    try:
        locator=(By.CLASS_NAME,"ewb-right-info")

        WebDriverWait(driver,2).until(EC.presence_of_all_elements_located(locator))
    except:
        locator=(By.XPATH,"//div[contains(@id,'menutab')][@style='']")

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
    if 'ewb-right-info' in page:
        div=soup.find('div',class_='ewb-right-info')
    else:
        div=soup.find("div",id=re.compile("menutab.*"),style='')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div



data = [
        ["gcjs_zhaobiao_gg","http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004001/004001001/004001001002/?Paging=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_biangeng_gg","http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004001/004001002/004001002002/?Paging=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zhongbiao_gg","http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004001/004001003/004001003002/?Paging=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_yucai_gg", "http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004001/004001005/004001005002/?Paging=1",
         ["name", "ggstart_time", "href","info"],f1,f2],


       ["zfcg_zhaobiao_gg", "http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004002/004002001/004002001002/?Paging=1",
        ["name", "ggstart_time", "href","info"],f1,f2],

       ["zfcg_biangeng_gg", "http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004002/004002002/004002002002/?Paging=1",
        ["name", "ggstart_time", "href","info"],f1,f2],

       ["zfcg_zhongbiao_gg", "http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004002/004002003/004002003002/?Paging=1",
        ["name", "ggstart_time", "href","info"],f1,f2],

       ["zfcg_yucai_gg","http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004002/004002005/004002005002/?Paging=1",
        ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_hetong_gg", "http://ll.dzzyjy.gov.cn/TPFront_laoling/xmxx/004002/004002006/004002006002/?Paging=1",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省乐陵市",num=5)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","leling"])

#est_tbs(conp=["postgres","since2015","127.0.0.1","shandong","leling"],data=data,total=1,num=1)