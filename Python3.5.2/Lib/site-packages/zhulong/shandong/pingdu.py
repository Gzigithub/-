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


_name_='pingdu'

def f1(driver, num):
    locator = (By.XPATH, "//table[@height='26']/tbody/tr[2]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "index.html" in url:
        cnum = 1
        url = re.sub("index_1", "index", url)
    else:
        cnum = int(re.findall("index_(\d+)", url)[0])
    if num != cnum:
        url = driver.current_url
        if num == 1:
            url = re.sub("index_[0-9]*", "index", url)
        elif "index.html" in url:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index", s, url)
        else:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index_(\d+)", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("//table[@height='26']/tbody/tr[2]/td/a").text
        
        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, '//td[@class="pagerTitle"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(r'(\d+)/', page_all)[0]
        if int(page) != num:
            locator = (By.XPATH, "//table[@height='26']/tbody/tr[2]/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    tb = soup.find("table", height="26", width="100%")
    trs = tb.find_all("tr")
    data = []
    for li in trs[1:]:
        # print(li)
        a = li.find("a")
        # print(a["title"])
        link = "http://zwgk.pingdu.gov.cn" + a["href"]
        span = li.find("td", width="80")
        tmp = [a.text.strip(), span.text.strip(), link]
        data.append(tmp)

        # print(data)
    df = pd.DataFrame(data=data)
    df["info"]=None
    return df




def f2(driver):

    locator = (By.XPATH, '//td[@class="pagerTitle"]')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = re.findall(r'/(\d+)', page_all)[0]

    driver.quit()
    return int(page)


def f3(driver,url):


    driver.get(url)

    locator=(By.ID,"Zoom")

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

    div=soup.find('div',id='Zoom')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div





data = [
        ["yuzhaobiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3591/index.html",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zhaobiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3592/index.html",
         ["name", "ggstart_time", "href","info"],f1,f2],


        ["zhongbiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3593/index.html",
         ["name", "ggstart_time", "href","info"],f1,f2],

    ]



def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省平度市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","pingdu"])

