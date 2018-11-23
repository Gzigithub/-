import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="haikou"


def zhaobiao_gg(f):
    def wrap(*krg):
        driver = krg[0]
        try:
            # 判断是否在交易信息栏里面
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
        except:
            # 在首页
            driver.switch_to.frame("mainFrame")
            locator = (By.XPATH, "(//a[@id='gcmore'])")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # 判断是否是招标公告
            # locator = (By.XPATH, "//li[@class='active']")
            # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(val)
            # if val != "招标公告":
            driver.execute_script("menuClick(this, 'GC_JY')")
        return f(*krg)
    return wrap


def zhongbiaohx_gg(f):
    def wrap(*krg):
        driver = krg[0]
        try:
            # 判断是否在交易信息栏里面
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
        except:
            # 在首页
            driver.switch_to.frame("mainFrame")
            locator = (By.XPATH, "(//a[@id='gcmore'])")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # 判断是否是招标公告
            # locator = (By.XPATH, "//li[@class='active']")
            # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(val)
            # if val != "招标公告":
            driver.execute_script("menuClick(this, 'GC_GS')")
        return f(*krg)

    return wrap



def zhongbiao_gg(f):
    def wrap(*krg):
        driver = krg[0]
        try:
            # 判断是否在交易信息栏里面
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
        except:
            # 在首页
            driver.switch_to.frame("mainFrame")
            locator = (By.XPATH, "(//a[@id='gcmore'])")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # 判断是否是招标公告
            # locator = (By.XPATH, "//li[@class='active']")
            # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(val)
            # if val != "招标公告":
            driver.execute_script("menuClick(this, 'GC_JG')")
        return f(*krg)

    return wrap



def zfcg_zhaobiao_gg(f):
    def wrap(*krg):
        driver = krg[0]
        try:
            # 判断是否在交易信息栏里面
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
        except:
            # 在首页
            driver.switch_to.frame("mainFrame")
            locator = (By.XPATH, "(//a[@id='zcmore'])")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # 判断是否是招标公告
            # locator = (By.XPATH, "//li[@class='active']")
            # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(val)
            # if val != "招标公告":
            driver.execute_script("menuClick(this, 'ZC_JY')")
        return f(*krg)

    return wrap



def zfcg_gg(f):
    def wrap(*krg):
        driver = krg[0]
        try:
            # 判断是否在交易信息栏里面
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator))
        except:
            # 在首页
            driver.switch_to.frame("mainFrame")
            locator = (By.XPATH, "(//a[@id='zcmore'])")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            # 判断是否是招标公告
            # locator = (By.XPATH, "//li[@class='active']")
            # val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            # print(val)
            # if val != "招标公告":
            driver.execute_script("menuClick(this, 'ZC_JG')")
        return f(*krg)

    return wrap


def f1(driver, num):
    print(num)
    # try:
    #     locator = (By.XPATH, "//ul[@class='info_list']/li[1]/div/a")
    #     val = WebDriverWait(driver, 2).until(EC.presence_of_element_located(locator)).text
    # except:
    #     driver.switch_to.frame("mainFrame")
    #     locator = (By.XPATH, "(//a[@id='gcmore'])")
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
    #     locator = (By.XPATH, "//ul[@class='info_list']/li[1]/div/a")
    #     val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    # driver.execute_script("menuClick(this, 'GC_JY')")
    locator = (By.XPATH, "//ul[@class='info_list']/li[1]/div/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//ul[@class='page']/li[2]/a")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+) \|', str)[0]

    if num != int(cnum):
        driver.execute_script("gotoPage({})".format(num))
        try:
            locator = (By.XPATH, "//ul[@class='info_list']/li[1]/div/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            time.sleep(2)


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    tbody = soup.find("ul", class_="info_list")

    trs = tbody.find_all("li")
    data = []
    i = 0
    for tr in trs:
        i += 1
        # onclick = a['onclick']
        # print(onclick)
        # driver.execute_script("".format(onclick))
        handle = driver.current_window_handle
        driver.find_element_by_xpath("//ul[@class='info_list']/li[{}]/div/a".format(i)).click()
        handles = driver.window_handles
        for newhandle in handles:
            if newhandle != handle:
                # 切换到新打开的窗口B
                driver.switch_to_window(newhandle)
                driver.close()
                driver.switch_to_window(handle)
        a = tr.find("a")
        driver.switch_to.frame("mainFrame")
        locator = (By.XPATH, "//ul[@class='info_list']/li[{}]/div/a".format(i))
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).get_attribute('href')
        # ActionChains(driver).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
        td = tr.find("div", class_='col2')
        tmp = [a["title"].strip(), td.text.strip(), link]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@class='page']/li[2]/a")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'\| (\d+)', str)[0]
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "head")

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

    div = soup.find('div', class_="content_wrap")


    return div


data = [
    ["gcjs_zhaobiao_gg", "http://ggzy.haikou.gov.cn/login.do?method=newindex",
     ["name", "ggstart_time", "href", "info"], zhaobiao_gg(f1), zhaobiao_gg(f2)],

    ["gcjs_zhongbiaohx_gg", "http://ggzy.haikou.gov.cn/login.do?method=newindex",
     ["name", "ggstart_time", "href", "info"], zhongbiaohx_gg(f1), zhongbiaohx_gg(f2)],

    ["gcjs_zhongbiao_gg", "http://ggzy.haikou.gov.cn/login.do?method=newindex",
     ["name", "ggstart_time", "href", "info"], zhongbiao_gg(f1), zhongbiao_gg(f2)],

    ["zfcg_zhaobiao_gg", "http://ggzy.haikou.gov.cn/login.do?method=newindex",
     ["name", "ggstart_time", "href", "info"], zfcg_zhaobiao_gg(f1), zfcg_zhaobiao_gg(f2)],

    ["zfcg_gg", "http://ggzy.haikou.gov.cn/login.do?method=newindex",
     ["name", "ggstart_time", "href", "info"], zfcg_gg(f1), zfcg_gg(f2)],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="海南省海口市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","hainan","haikou"])



    # driver=webdriver.Chrome()
    # url="http://ggzy.haikou.gov.cn/login.do?method=newindex"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    # for i in range(1, 5):
    #     df=zfcg_gg(f1)(driver, i)
    #     print(df)
