import time

import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)
from zhulong import gg_meta, gg_html


def f1(driver, num):
    print(num)
    locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//div[@class='pagesite']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]
    # print(cnum)

    if num != int(cnum):
        if num == 1:
            driver.execute_script("location.href=encodeURI('index.jhtml');")
        else:
            driver.execute_script("location.href=encodeURI('index_{}.jhtml');".format(num))

        locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a[string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table= soup.find("table", class_="newtable")

    tbody = table.find("tbody")

    trs = tbody.find_all("tr")
    data = []
    for tr in trs[:-1]:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            continue
        tds = tr.find_all("td")[2].text
        td = re.findall(r"\[(.*)\]", tds)[0]
        tmp = [a["title"].strip(), td.strip(), link.strip()]
        data.append(tmp)



    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    # driver.set_page_load_timeout(30)
    # driver.maximize_window()
    # driver.execute_script("location.reload()")
    # html = driver.page_source
    # if html:
    #     pass
    # else:
    # driver.refresh()
    locator = (By.XPATH, "//table[@class='newtable']/tbody/tr[1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//div[@class='pagesite']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "navBar")

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

    div = soup.find('div', class_="newsTex")


    return div


data = [
    ["gcjs_zhaobiao_gg", "http://zw.hainan.gov.cn/ggzy/dzggzy/GGjxzbgs1/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg", "http://zw.hainan.gov.cn/ggzy/dzggzy/GGjxzbgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg", "http://zw.hainan.gov.cn/ggzy/dzggzy/GGZFZBGS/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg", "http://zw.hainan.gov.cn/ggzy/dzggzy/GGZFZBGS1/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp):
    gg_meta(conp,data=data,diqu="海南省儋州市")

    gg_html(conp,f=f3)



if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","hainan","danzhou"]

    work(conp=conp)
    #
    # driver=webdriver.Chrome()
    # url="http://zw.hainan.gov.cn/ggzy/dzggzy/GGjxzbgs1/index.jhtml"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 5):
    #     df=f1(driver, i)
    #     print(df)
