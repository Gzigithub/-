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


_name_="hangzhou"





# def f1_data(driver):
#     url_1 = "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=27&proID=&title="
#     driver.get(url_1)
#     cnum = f2_data(driver)
#     driver.back()
#     return cnum


def f1(driver, num):
    # print(num_list)
    url = driver.current_url

    locator = (By.XPATH, "//*[@id='1']/td[4]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    if num != 1:
        driver.find_element_by_xpath('//input[@class="ui-pg-input"]').clear()
        driver.find_element_by_xpath('//input[@class="ui-pg-input"]').send_keys(num, Keys.ENTER)
        try:
            locator = (By.XPATH, "//*[@id='1']/td[4]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//*[@id='1']/td[4]/a[string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("table", id="gridData")

    trs = tbody.find_all("tr", class_='ui-widget-content jqgrow ui-row-ltr')
    data = []
    for tr in trs:
        TenderNo = tr.find("td", attrs={'aria-describedby':'gridData_TenderNo'})
        a = tr.find("a")
        if "moduleID=67&ViewID=17&areaID=" in url:
            link = a['href'].strip()
        else:
            ModuleID = int(re.findall(r'afficheType=(\d+)', url)[0])
            links = a['href'].strip()
            link = re.sub('ModuleID=undefined', 'ModuleID={}'.format(ModuleID), links)

        td = tr.find("td", attrs={'aria-describedby':'gridData_PublishStartTime'})
        tmp = [TenderNo.text.strip(), a.text.strip(), td.text.strip(), "http://www.hzctc.cn"+link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2_data(driver):
    locator = (By.XPATH, '//*[@id="1"]/td[4]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, '//*[@id="sp_1_gridPager"]')
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    if ',' in str:
        num = re.sub(',', '', str)
    else:
        num = int(str.strip())
    return num


def f2(driver):

    num = f2_data(driver)

    driver.quit()
    return int(num)



def gcjs_gg(f):
    def wrap(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//div[@class='term_list gglx']/dl/dd[@class='selected']")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        if "开标结果公示" not in val:
            nname = driver.find_element_by_xpath("//div[@class='term_list gglx']/dl/dd[string()='开标结果公示']").click()
            locator = (By.XPATH, "//div[@class='term_list gglx']/dl/dd[@class='selected'][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        driver.switch_to.frame("DataList")

        return f(*krg)

    return wrap





def f3(driver, url):
    driver.get(url)

    try:
        locator = (By.CLASS_NAME, "banner")
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(locator))
    except:
        html_data = driver.page_source
        if "信息当前尚未发布或发布已截止" in html_data:
            return
        locator = (By.CLASS_NAME, "banner")
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(locator))


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

    div = soup.find('div', class_='MainList')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?title=&area=&afficheType=22",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://www.hzctc.cn/SecondPage/SecondPage?moduleID=67&ViewID=17&areaID=",
     ["prj_number", "name", "ggstart_time", "href", "info"],gcjs_gg(f1),gcjs_gg(f2)],

    ["gcjs_zhongbiaohx_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=25&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=28&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=27&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_danyilaiyuan_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=26&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"], f1, f2],


    ["zfcg_biangen_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=29&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=32&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhaobiao_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=34&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhongbiaohx_gg",
     "http://www.hzctc.cn/SecondPage/ProjectAfficheList?area=&afficheType=37&proID=&title=",
     ["prj_number", "name", "ggstart_time", "href", "info"],f1,f2],

]



def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省杭州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","hangzhou"])


    # driver=webdriver.Chrome()
    # url="http://www.hzctc.cn/SecondPage/SecondPage?moduleID=67&ViewID=17&areaID="
    # driver.get(url)
    #
    # locator = (By.XPATH, "//div[@class='term_list gglx']/dl/dd[@class='selected']")
    # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    # print(val)
    # if "开标结果公示" not in val:
    #     nname = driver.find_element_by_xpath("//div[@class='term_list gglx']/dl/dd[string()='开标结果公示']").click()
    #     locator = (By.XPATH, "//div[@class='term_list gglx']/dl/dd[@class='selected'][string()!='%s']" % val)
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # driver.switch_to.frame("DataList")
    # df = f2(driver)
    # print(df)
    # for i in range(158, 161):
    #     df=f1(driver, i)
    #     print(df)
