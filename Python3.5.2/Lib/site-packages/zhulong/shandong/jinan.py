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

from zhulong.util.etl import est_tables,gg_meta,gg_html,est_meta,est_html


_name_='jinan'

def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    cnum = driver.find_element_by_xpath('//*[@id="pag"]').text

    # val = driver.find_element_by_xpath("//ul[@class='ewb-info-list']//li[1]//a").text
    if cnum != num:
        driver.find_element_by_xpath('//*[@id="toPageNum"]').clear()
        driver.find_element_by_xpath('//*[@id="toPageNum"]').send_keys(num)
        driver.find_element_by_xpath('//*[@id="part4"]/span[8]').click()
        locator = (By.XPATH, "//*[@id='content']/ul/li[1]/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("div", id="content")
    lis = ul.find_all("li")
    data = []
    for li in lis:
        a = li.find("a")
        title = a["title"]
        try:
            a_nunm = a["onclick"]
            a_num = re.findall('\((.*)\)', a_nunm)[0]
            link = "http://jnggzy.jinan.gov.cn/jnggzyztb/front/showNotice.do?iid={}&xuanxiang=".format(a_num)
        except:
            link = "http://jnggzy.jinan.gov.cn" + a["href"]

        span1 = li.find("span", class_="span1")
        span2 = li.find("span", class_="span2")
        tmp = [span1.text.strip(), title.strip(), span2.text.strip(), link]
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
    locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, '//*[@id="part4"]/span[7]')
        WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).click()
        locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
        val = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text
        if val:
            locator = (By.XPATH, '//*[@id="apagesum"]')
            page = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text

    except Exception as e:
        driver.refresh()
        i = 1
        while True:
            i += 1
            locator = (By.XPATH, '//*[@id="part4"]/span[6]')
            WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).click()
            try:
                locator = (By.XPATH, '//*[@id="content"]/ul/li[1]/a')
                val = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text
            except:
                page = (i - 1)
                break
    driver.quit()

    return int(page)

def add_info(f,info):
    def wrap(*arg):
        df=f(*arg)
        df["info"]=json.dumps(info,ensure_ascii=False)
        return df 
    return wrap

def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"list")

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

    div=soup.find('div',class_='list')
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return div


data = [
        ["gcjs_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["gcjs_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_biangeng_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=3&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["zfcg_feibiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=1&xuanxiang=4&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["qsydw_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=7&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],
        ["qsydw_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=7&xuanxiang=2&area=",
         ["place", "name", "ggstart_time", "href","info"],f1,f2],

        ["gcjs_shuili_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=4&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"水利"}),f2],
        ["gcjs_shuili_zhongbiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=4&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"水利"}),f2],

        ["gcjs_tielu_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=5&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"铁路"}),f2],
        ["gcjs_tielu_zhongbiao_gg",
         "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=5&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"铁路"}),f2],
        ["gcjs_tielu_zhongbiaohx_gg",
         "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=5&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"铁路"}),f2],

        ["gcjs_jiaotong_zhaobiao_gg", "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=6&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"交通"}),f2],
        ["gcjs_jiaotong_zhongbiao_gg",
         "http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=6&xuanxiang=1&area=",
         ["place", "name", "ggstart_time", "href","info"],add_info(f1,{"gctype":"交通"}),f2],

    ]


# url="http://jnggzy.jinan.gov.cn/jnggzyztb/front/noticelist.do?type=0&xuanxiang=1&area="
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

#est_tables(conp=["postgres","since2015","192.168.3.172","shandong","jinan"],data=data)


def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省济南市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    work(conp=["postgres","since2015","127.0.0.1","shandong","jinan"])