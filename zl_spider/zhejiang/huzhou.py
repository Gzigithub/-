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

from zhulong.util.etl import add_info,est_meta,est_html,est_tbs


_name_="huzhou"



# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)



def f1(driver, num):

    locator = (By.XPATH, "(//a[@class='WebList_sub'])[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//td[@class='huifont']")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]

    url = driver.current_url
    if num != int(cnum):
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//a[@class='WebList_sub'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "(//a[@class='WebList_sub'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("table", width='98%')

    trs = table.find_all("tr", height="24")
    data = []
    for tr in trs[1:]:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            link = ''
        td = tr.find("td", width="80").text
        tmp = [a["title"].strip(), td.strip(), "http://ggzy.huzhou.gov.cn" + link.strip()]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, "(//a[@class='WebList_sub'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, '//td[@class="huifont"]')
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    num = re.findall(r'/(\d+)', str)[0]

    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "bg")

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

    div = soup.find('td', height='500')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_jianshe_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001001/029001001001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_jianshe_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001001/029001001002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_jiaotong_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001002/029001002001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_jiaotong_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001002/029001002002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_shuili_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001003/029001003001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_shuli_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001003/029001003002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_xianer_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001004/029001004001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_jizhong_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004001/029004001001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jizhong_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004001/029004001002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jizhong_yucai_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004001/029004001003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_fensan_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004002/029004002001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_fensan_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004002/029004002002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],
    ["zfcg_fensan_yucai_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004002/029004002003/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_xieyi_cheliangweixiu_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004004/029004004001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_jizhong_caigoumulu_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029004/029004005/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["ylcg_jizhong_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029005/029005001/029005001001/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["ylcg_jizhong_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029005/029005001/029005001002/?Paging=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["ylcg_fensan_zhaobiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029005/029005002/029005002001/?Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["ylcg_fensan_zhongbiao_gg",
     "http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029005/029005002/029005002002/?Paging=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省湖州市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","huzhou"])


    # driver=webdriver.Chrome()
    # url="http://ggzy.huzhou.gov.cn/HZfront/jyxx_HuZhou/029001/029001001/029001001001/?Paging=1"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)
