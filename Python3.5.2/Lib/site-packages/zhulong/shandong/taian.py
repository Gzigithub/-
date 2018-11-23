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

from zhulong.util.etl import gg_html,gg_meta,est_tables,est_html,est_meta

_name_='taian'
def f1(driver, i):
    url_i = driver.current_url
    # print(url_i)
    if "Paging" not in url_i:
        # print(url)
        url_2 = url_i.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        url_1 = url_2 + "/?Paging={}".format(i)
        # print(url_1)
        driver.get(url_1)
    else:
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(i), url_i)
        val = driver.find_element_by_xpath('//*[@id="right_table"]/table/tbody/tr[1]/td[2]/a').text
        # print(url_1)
        driver.get(url_1)
        locator = (By.XPATH, "//*[@id='right_table']/table/tbody/tr[1]/td[2]/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, '(//a[@class="WebList_sub"])[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("div", id="right_table")
    # tb = ul.find_all("table",recursive=False)[0]
    lis = ul.find_all("tr", height='30')
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://www.taggzyjy.com.cn" + a["href"]
        span = li.find("td", width='80').text.strip()
        span_1 = re.findall(r"\[(.*)\]", span)[0]
        tmp = [title, span_1, link]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"]=None


    return df




def f2(driver):
    locator = (By.ID, "right_table")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//td[@class='huifont']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    txt=driver.find_element_by_xpath("//td[@class='huifont'][contains(string(),'/')]").text

    total=txt.split("/")[1]
    total=int(total)
    driver.quit()
    return total


def add_info(f,info):
    def wrap(*arg):
        df=f(*arg)
        df["info"]=json.dumps(info,ensure_ascii=False)
        return df 
    return wrap


def f3(driver,url):


    driver.get(url)

    locator=(By.CLASS_NAME,"inner")

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

    div=soup.find('div',class_='inner')
    td=div.find("td",width="998")
    #div=div.find_all('div',class_='ewb-article')[0]
    
    return td


data = [
        #工程建设-招标公告
        ["gcjs_zhaobiao_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],

        ["gcjs_zhaobiao_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001002/075001001002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],


        ["gcjs_zhaobiao_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001002/075001001002002/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],


        ["gcjs_zhaobiao_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001002/075001001002003/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["gcjs_zhaobiao_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["gcjs_zhaobiao_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["gcjs_zhaobiao_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["gcjs_zhaobiao_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["gcjs_zhaobiao_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],


         #工程建设-中标公告
        ["gcjs_zhongbiaohx_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],



        ["gcjs_zhongbiaohx_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002002/075001002002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],

        ["gcjs_zhongbiaohx_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002002/075001002002002/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],

        ["gcjs_zhongbiaohx_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002002/075001002002003/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["gcjs_zhongbiaohx_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["gcjs_zhongbiaohx_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["gcjs_zhongbiaohx_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["gcjs_zhongbiaohx_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["gcjs_zhongbiaohx_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],


         #工程建设变更公告
        ["gcjs_bianggen_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],

        # ["gcjs_bianggen_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002002/075001002002001/",
        #  ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],

        ["gcjs_bianggen_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003002/075001003002002/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],

        # ["gcjs_bianggen_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001002/075001002002/075001002002003/",
        #  ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["gcjs_bianggen_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["gcjs_bianggen_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["gcjs_bianggen_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["gcjs_bianggen_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["gcjs_bianggen_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075001/075001003/075001003008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],


         #政府采购-招标公告
        ["zfcg_zhaobiao_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],


        ["zfcg_zhaobiao_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001002/075002001002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],

        # ["zfcg_zhaobiao_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001002/075002001002002/",
        #  ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],

        ["zfcg_zhaobiao_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001002/075002001002003/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["zfcg_zhaobiao_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["zfcg_zhaobiao_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["zfcg_zhaobiao_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["zfcg_zhaobiao_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["zfcg_zhaobiao_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002001/075002001008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],


         #政府采购-中标标公告
        ["zfcg_zhongbiaohx_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],


        ["zfcg_zhongbiaohx_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002002/075002002002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],

        # ["zfcg_zhongbiaohx_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002002/075002002002002/",
        #  ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],

        ["zfcg_zhongbiaohx_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002002/075002002002003/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["zfcg_zhongbiaohx_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["zfcg_zhongbiaohx_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["zfcg_zhongbiaohx_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["zfcg_zhongbiaohx_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["zfcg_zhongbiaohx_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002002/075002002008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],


         #政府采购-变更公告
        ["zfcg_bianggen_diqu1_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市本级"}),f2],


        ["zfcg_bianggen_diqu21_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003002/075002003002001/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山区"}),f2],

        # ["zfcg_bianggen_diqu22_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003002/075002003002002/",
        #  ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-高新区"}),f2],

        ["zfcg_bianggen_diqu23_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003002/075002003002003/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"市-泰山景区"}),f2],

        ["zfcg_bianggen_diqu3_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003004/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"新泰市"}),f2],

        ["zfcg_bianggen_diqu4_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003005/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"肥城市"}),f2],

        ["zfcg_bianggen_diqu5_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003006/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"宁阳县"}),f2],

        ["zfcg_bianggen_diqu6_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003007/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"东平县"}),f2],

        ["zfcg_bianggen_diqu7_gg", "http://www.taggzyjy.com.cn/Front/jyxx/075002/075002003/075002003008/",
         ["name", "ggstart_time", "href","info"],add_info(f1,{"diqu":"岱岳区"}),f2],




    ]



# driver=webdriver.Chrome()
# url="http://www.taggzyjy.com.cn/Front/jyxx/075001/075001001/075001001001/"
# driver.get(url)
# est_tables(conp=["postgres","since2015","127.0.0.1","shandong","taian"],data=data[-6:])
# gg(conp=["postgres","since2015","127.0.0.1","shandong","taian"],diqu="山东省泰安市")

def work(conp,**args):
    est_meta(conp,data=data,diqu="山东省泰安市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

# for _ in range(2):
#     work(conp=["postgres","since2015","127.0.0.1","shandong","taian"])

    work(conp=["postgres","since2015","127.0.0.1","shandong","taian"])

