
import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

import json


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="linhai"




def f1(driver, num):
    url = driver.current_url
    if "whichPage" in url:
        html = driver.find_element_by_xpath('//pre').text
        # print(html)
        html_json = json.loads(html)
        html_data = html_json['params']['listInfo']
        soup = BeautifulSoup(html_data, 'lxml')
        cnum = soup.find("span", id="pageone1Notice").text.strip()
        if num != int(cnum):
            if num == 1:
                url = re.sub("whichPage=[0-9]*", "whichPage=1", url)
            else:
                s = "whichPage=%d" % (num) if num > 1 else "whichPage=1"
                url = re.sub("whichPage=[0-9]*", s, url)
                # print(cnum)
            driver.get(url)
            html = driver.find_element_by_xpath('//pre').text
            # print(html)
            html_json = json.loads(html)
            html_data = html_json['params']['listInfo']
            soup = BeautifulSoup(html_data, 'lxml')

        cataId = re.findall(r'cataId=(\d+)', url)[0]

        table = soup.find("td", align="center", valign="top")

        trs = table.find_all("table")
        data = []
        for tr in trs:
            a = tr.find("a")
            try:
                title = a["title"].strip()
            except:
                title = a.text.strip()
            try:
                link = a["href"]
            except:
                continue
            td = tr.find("td", width="102").text.strip()
            td = re.findall(r'\[(.*)\]', td)[0]

            link = "http://183.131.114.214:8082" + link.strip()

            link = re.sub('cataid=(\d+)', "cataid="+cataId, link)

            tmp = [title, td, link]
            data.append(tmp)

        df = pd.DataFrame(data)
        df['info'] = None
        return df

    locator = (By.XPATH, "//*[@id='container_liucheng']/table/tbody/tr[2]/td/table[1]/tbody/tr[1]/td[2]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//span[@id='pageone1']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = str.strip()
    except:
        cnum = 1

    url = driver.current_url

    if num != int(cnum):
        if num == 1:
            url = re.sub("startPage=[0-9]*", "startPage=1", url)
        else:
            s = "startPage=%d" % (num) if num > 1 else "startPage=1"
            url = re.sub("startPage=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "//*[@id='container_liucheng']/table/tbody/tr[2]/td/table[1]/tbody/tr[1]/td[2]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//*[@id='container_liucheng']/table/tbody/tr[2]/td/table[1]/tbody/tr[1]/td[2]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("td", align="center", valign="top")

    trs = table.find_all("table")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            title = a["title"].strip()
        except:
            title = a.text.strip()
        try:
            link = a["href"]
        except:
            link = ''
        td = tr.find("td", width="102").text.strip()
        td = re.findall(r'\[(.*)\]', td)[0]

        link = "http://183.131.114.214:8082"+link.strip()

        tmp = [title, td, link]
        data.append(tmp)



    df = pd.DataFrame(data)
    df['info'] = None
    return df





def f2(driver):
    url = driver.current_url
    if "whichPage" in url:
        whichPage = 1
        html = driver.find_element_by_xpath('//pre').text
        # print(html)
        html_json = json.loads(html)
        html_data = html_json['params']['listInfo']
        soup = BeautifulSoup(html_data, 'lxml')
        span = soup.find("span", id="pageCountNotice")
        num = span.text.strip()
        driver.quit()
        return int(num)


    locator = (By.XPATH, "//*[@id='container_liucheng']/table/tbody/tr[2]/td/table[1]/tbody/tr[1]/td[2]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//span[@id='pageCount']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(str.strip())
    except:
        num = 1

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "wrap1")

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div = soup.find('div', class_="lists")
    # div=div.find_all('div',class_='ewb-article')[0]

    return div






data = [

    ["gcjs_yuzhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/show_list.do?type=8801&startPage=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9911&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9913&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zishenjieguo_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9916&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9912&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["gcjs_zhongbiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9915&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_yanshou_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9914&whichPage=1&searchInfo=&type=8801",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yuzhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/show_list.do?type=8802&startPage=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9928&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9921&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9923&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zishenjieguo_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9926&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiaohx_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9922&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9925&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_yanshou_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9924&whichPage=1&searchInfo=&type=8802",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_xiaoer_yuzhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/show_list.do?type=8807&startPage=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_zhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9971&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9973&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_zishenjieguo_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9976&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_zhongbiaohx_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9972&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_zhongbiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9975&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_xiaoer_yanshou_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9974&whichPage=1&searchInfo=&type=8807",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_zhaobiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9951&whichPage=1&searchInfo=&type=8805",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9953&whichPage=1&searchInfo=&type=8805",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiaohx_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9952&whichPage=1&searchInfo=&type=8805",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9955&whichPage=1&searchInfo=&type=8805",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省临海市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","linhai"],num=10)


    # driver=webdriver.Chrome()
    # url="http://183.131.114.214:8082/lhggzyqlc/front/out_notice.do?cataId=9916&whichPage=1&searchInfo=&type=8801"
    # # url = "http://183.131.114.214:8082/lhggzyqlc/front/show_list.do?type=8801&startPage=1"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
