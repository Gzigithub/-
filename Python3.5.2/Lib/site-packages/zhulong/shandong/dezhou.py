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

from zhulong.util.etl import est_tables,gg_html,gg_meta


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]


_name_="dezhou"


def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//td[2])[1]')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # 获取当前页的url
    url = driver.current_url
    # print(url)
    cnum = int(re.findall("Paging=(.*)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//td[2])[1]").text

        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall('(.*)/', page_all)[0]
        if int(page) != num:
            locator = (By.XPATH, "(//td[2])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", class_="ewb-right-info")
    tb = ul.find_all("div", recursive=False)[0]
    lis = tb.find_all("tr")
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")
        title = a["title"]
        # print(a["title"])
        link = "http://www.dzzyjy.gov.cn" + a["href"]
        span = li.find("font")
        tmp = [title, span.text.strip(), link]
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
    # locator = (By.XPATH, '(//td[2])[1]')
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        # print(url)
        page = re.findall('/(.*)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
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
    ["gcjs_yucai_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001005/004001005001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["gcjs_zhaobiao_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001001/004001001001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["gcjs_biangeng_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001002/004001002001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["gcjs_zhongbiaohx_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001008/004001008001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["gcjs_zhongbiao_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001003/004001003001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["gcjs_hetong_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004001/004001006/004001006001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["zfcg_zhaobiao_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004002/004002001/004002001001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["zfcg_biangeng_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004002/004002002/004002002001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["zfcg_zhongbiao_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004002/004002003/004002003001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["zfcg_yucai_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004002/004002005/004002005001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],
    ["zfcg_hetong_gg", "http://www.dzzyjy.gov.cn/TPFront/xmxx/004002/004002006/004002006001/?Paging=1",
     ["name", "ggstart_time", "href","info"],f1,f2],

]


# est_tables(conp=["postgres","since2015","192.168.3.172","shandong","dezhou"],data=data[4:])
# url="http://www.dzzyjy.gov.cn/TPFront/ZtbInfo/ZtbDyDetail_zfcg.aspx/?InfoID=ec08f536-bcc1-406e-ba6c-8cec1340a1e9&type=3&categoryNum=004002003001"


# driver=webdriver.Chrome()

# driver.get(url)

def work(conp,**args):
    gg_meta(conp,data=data,diqu="山东省德州市",**args)
    gg_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","dezhou"])

#work(conp=["postgres","since2015","127.0.0.1","shandong","dezhou"])

#work(conp=["postgres","since2015","127.0.0.1","shandong","dezhou"])



