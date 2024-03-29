import random

import pandas as pd
import re

import requests
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
from fake_useragent import agents
import json



from zhulong.util.etl import add_info,est_meta,est_html,est_tbs

_name_="jianou"


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1_requests(datas, start_url, s=0):
    user_agent = random.choice(agents)
    headers = {
        'User-Agent': user_agent,
    }

    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=datas)
    # 需要判断是否为登录后的页面
    if res.status_code == 200:
        html = res.text
        if html:
            html = json.loads(html)
            datalist = html["data"]
            data_list = []
            for data in datalist:
                if s == 3:
                    title = data['TITLE']
                    td = data['TM']
                    link = "http://www.joztb.com/views/tradeCenter/jianou/trade.html?id="+data['ID']+"&type=articles&ons=%E4%B9%A1%E9%95%87%E6%8B%9B%E6%A0%87"
                    tmp = [title, td, link]
                    data_list.append(tmp)
                else:
                    title = data['NAME']
                    td = data['PUBLISHED_TIME']
                    link = data['URL']
                    if s == 2:
                        link = link.strip() + "/zhongbiaogg"

                    tmp = [title, td, link]
                    data_list.append(tmp)

            df = pd.DataFrame(data_list)
            df['info'] = None
            return df



def f1(driver, num):
    url = driver.current_url
    if "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A" in url:
        datas = {
            'method': 'Web.GetJiaoYiList',
            'pageindex': '{}'.format(num),
            'pagesize': '15',
            'BIG_TYPE': 'A',
            'NAME': '',
            'TYPE': '',
            'AREA_CODE': '35',
            'PUBLISHED_TIME_START': '2016-11-01',
            'PUBLISHED_TIME_END': '2018-11-23',
            'STATUS': '',
        }
        start_url = "http://www.enjoy5191.com:9001/api/GetDataHandler.ashx?PLATFORM_CODE=E3507837011"
        df = f1_requests(datas, start_url, s=2)
        return df

    elif "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E4%B8%AD%E6%A0%87%E5%85%AC%E7%A4%BA" in url:
        datas = {
            'method': 'Web.GetJiaoYiList',
            'pageindex': '{}'.format(num),
            'pagesize': '15',
            'BIG_TYPE': '',
            'NAME': '',
            'TYPE': '',
            'AREA_CODE': '',
            'PUBLISHED_TIME_START': '',
            'PUBLISHED_TIME_END': '',
            'STATUS': '',
            'in_status': '3,4'
        }
        start_url = "http://www.enjoy5191.com:9001/api/GetDataHandler.ashx?PLATFORM_CODE=E3507837011"
        df = f1_requests(datas, start_url, s=2)
        return df

    else:
        datas = {
            'method':'Web.GetNewsList',
            'in_type':'73e4fff0-9a96-42d9-8300-542d29c22b06',
            'pageindex': '{}'.format(num),
            'pagesize':'15',
            'TITLE':'',
            'CREATE_TM_START':'1900-01-01',
            'CREATE_TM_END':'2018-11-23',
        }
        start_url = "http://www.enjoy5191.com:9001/api/GetDataHandler.ashx?PLATFORM_CODE=E3507837011"
        df = f1_requests(datas, start_url, s=3)
        return df


def f2_requests(data, start_url):
    user_agent = random.choice(agents)
    headers = {
        'User-Agent': user_agent,
    }

    sesion = requests.session()
    res = sesion.post(url=start_url, headers=headers, data=data)
    # 需要判断是否为登录后的页面
    if res.status_code == 200:
        html = res.text
        if html:
            html = json.loads(html)
            total = html["total"]
            # print(total / 20)
            if total/15 == int(total/15):
                page_all = int(total/15)
            else:
                page_all = int(total/15) + 1
            return page_all



def f2(driver):
    url = driver.current_url
    if "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A" in url:
        data = {
            'method': 'Web.GetJiaoYiList',
            'pageindex': '1',
            'pagesize': '15',
            'BIG_TYPE': 'A',
            'NAME': '',
            'TYPE': '',
            'AREA_CODE': '35',
            'PUBLISHED_TIME_START': '2016-11-01',
            'PUBLISHED_TIME_END': '2018-11-23',
            'STATUS': '',
        }
        start_url = "http://www.enjoy5191.com:9001/api/GetDataHandler.ashx?PLATFORM_CODE=E3507837011"
        num_total = f2_requests(data, start_url)
        driver.quit()
        return int(num_total)

    try:
        locator = (By.XPATH, "//span[@class='pageInfo']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num_total = re.findall(r'(\d+)', str)[0]
    except:
        num_total = 1

    driver.quit()
    return int(num_total)




def f3(driver, url):

    if "/zhongbiaogg" in url:
        url = url.rsplit('/', maxsplit=1)[0]
        driver.get(url)
        try:
            locator = (By.XPATH, "//*[contains(text(),'中标公示')]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        except:
            locator = (By.XPATH, "//*[contains(text(),'中标公告')]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()

        time.sleep(1)
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

        div = soup.find('iframe')
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    driver.get(url)
    if "http://106.75.116.110:8210/fjebid/jypt.html?" in url:

        locator = (By.CLASS_NAME, "main")
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

        div = soup.find('div', style="overflow:hidden;height:100%")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "4008705191.cn/views" in url:
        locator = (By.CLASS_NAME, "app")
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

        div = soup.find('div', style="overflow: hidden; height: 100%;")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "4008705191.cn:5000/views" in url:
        locator = (By.CLASS_NAME, "app")
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

        div = soup.find('div', style="overflow: hidden; height: 100%;")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    elif "http://www.joztb.com/views/tradeCenter/jianou/" in url:
        locator = (By.CLASS_NAME, "app")
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

        div = soup.find('div', class_="el-col el-col-24")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div

    else:

        locator = (By.ID, "mainFrame")
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

        div = soup.find('div', id="cDivr")
        # div=div.find_all('div',class_='ewb-article')[0]

        return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E6%8B%9B%E6%A0%87%E5%85%AC%E5%91%8A",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zhongbiao_gg",
     "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E4%B8%AD%E6%A0%87%E5%85%AC%E7%A4%BA",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["xiangzhen_gg",
     "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E4%B9%A1%E9%95%87%E6%8B%9B%E6%A0%87",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="福建省建瓯市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","jianou"])


    #
    # driver=webdriver.Chrome()
    # url = "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E4%B8%AD%E6%A0%87%E5%85%AC%E7%A4%BA"
    # driver.get(url)
    # d = f3(driver, "http://qtgcztb.4008705191.cn/views/ebid/combine/v1/entp-view.html?type=tp&tpId=5bcd81ef8b91863e780920d7&flag=true/zhongbiaogg")
    # print(d)
    # df = f2(driver)
    # print(df)
    # driver = webdriver.Chrome()
    # url = "http://www.joztb.com/views/tradeCenter/jianou/trade.html?type=%E4%B9%A1%E9%95%87%E6%8B%9B%E6%A0%87"
    # driver.get(url)
    #
    # for i in range(1, 33):
    #     df=f1(driver, i)
    #     print(df)
