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


from zhulong.util.etl import est_tables,gg_html,gg_meta,est_meta,est_html

_name_='zaozhuang'


def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    # 获取当前页的url
    url = driver.current_url
    if "Paging" in url:
        # print(url)
        url_3 = url.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        driver.get(url_3)
    html = driver.page_source
    if "本栏目信息正在更新中" in html:
        print("本栏目信息正在更新中,err_url:{}".format(url))

    url_i = driver.current_url
    # print(url_i)
    if "Paging" not in url_i:
        # print(url)
        url_2 = url_i.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        url_1 = url_2 + "/?Paging={}".format(num)
        # print(url_1)
        driver.get(url_1)
    else:
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(num), url_i)
        val = driver.find_element_by_xpath('(//table[@align="center"]/tbody/tr/td/a)[1]').text
        # print(url)
        driver.get(url_1)
        locator = (By.XPATH, "(//table[@align='center']/tbody/tr/td/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # print(url_1)
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("table", align="center", width='98%')
    lis = ul.find_all("tr", height='30')
    data = []
    for li in lis[:-2]:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://www.zzggzy.com" + a["href"]
        span = li.find("td", width='90').text
        span = re.findall(r"\[(.*)\]", span)[0]
        tmp = [title, span.strip(), link]
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
    try:
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall('/(\d+)', page_all)[0]
    except Exception as e:
        html = driver.page_source
        if "本栏目信息正在更新中" in html:
            page = 1
    driver.quit()
    return int(page)


def f3(driver,url):


    driver.get(url)

    locator=(By.XPATH,"//td[@height='500']")

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

    div=soup.find('td',height="500")
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div


data = [

        ["gcjs_zhaobiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001001/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_weiruwei_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001003/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_zhongbiaohx_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001004/",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_zhongbiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001005/",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_biangeng_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001008/",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_biangeng_gg", "http://www.zzggzy.com/TPFront/jyxx/070001/070001008/",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["zfcg_yucai_gg", "http://www.zzggzy.com/TPFront/jyxx/070002/070002004/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhaobiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070002/070002001/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_biangeng_gg", "http://www.zzggzy.com/TPFront/jyxx/070002/070002002/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhongbiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070002/070002003/",
         ["name", "ggstart_time", "href","info"],f1,f2],

        ["qsydw_zhaobiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070004/070004001/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["qsydw_biangeng_gg", "http://www.zzggzy.com/TPFront/jyxx/070004/070004002/",
         ["name", "ggstart_time", "href","info"],f1,f2],
        ["qsydw_zhongbiao_gg", "http://www.zzggzy.com/TPFront/jyxx/070004/070004003/",
         ["name", "ggstart_time", "href","info"],f1,f2],
    ]


#est_tables(conp=["postgres","since2015","192.168.3.172","shandong","zaozhuang"],data=data)

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东枣庄市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","shandong","zaozhuang"])