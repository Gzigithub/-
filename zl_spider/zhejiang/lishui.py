from os.path import dirname, join

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
from zhulong.util.etl import add_info, est_meta, est_html, est_tbs, gg_existed

_name_="lishui"

# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

num_list = []




def f1_data(driver, cnum, stitle):
    locator = (By.XPATH, "(//td[@class='LeftMenuJsgc'])[{}]".format(cnum))
    jtitle = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    if stitle != jtitle:
        driver.find_element_by_xpath("(//td[@class='LeftMenuJsgc'])[{}]".format(cnum)).click()
        locator = (By.XPATH, "(//font[@class='currentpostionfont'])[last()][contains(text(),'%s')]" % jtitle)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


def f1(driver, num):
    # print(num)
    # print(num_list)
    url = driver.current_url
    if ("http://www.lssggzy.com/lsweb/jyxx/071002/071002008" not in url) and ("http://www.lssggzy.com/lsweb/jyxx/071002/071002009" not in url):
        locator = (By.XPATH, "(//font[@class='currentpostionfont'])[last()]")
        stitle = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

        if num <= num_list[0]:
            num = num
            f1_data(driver, 1, stitle)

        elif num_list[0] < num <= num_list[1]:
            num = num - num_list[0]
            f1_data(driver, 2, stitle)

        elif num_list[1] < num <= num_list[2]:
            num = num - num_list[1]
            f1_data(driver, 3, stitle)

        elif num_list[2] < num <= num_list[3]:
            num = num - num_list[2]
            f1_data(driver, 4, stitle)

        elif num_list[3] < num <= num_list[4]:
            num = num - num_list[3]
            f1_data(driver, 5, stitle)

        elif num_list[4] < num <= num_list[5]:
            num = num - num_list[4]
            f1_data(driver, 6, stitle)

        elif num_list[5] < num <= num_list[6]:
            num = num - num_list[5]
            f1_data(driver, 7, stitle)

        elif num_list[6] < num <= num_list[7]:
            num = num - num_list[6]
            f1_data(driver, 8, stitle)

        elif num_list[7] < num <= num_list[8]:
            num = num - num_list[7]
            f1_data(driver, 9, stitle)

        elif num_list[8] < num <= num_list[9]:
            num = num - num_list[8]
            f1_data(driver, 10, stitle)

    # 进行增量更新,只获取前10页
    if num > CDC_NUM:
        return

    try:
        locator = (By.XPATH, "(//tr[@height='25']/td/a)[1]")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    except:
        html_data = driver.page_source
        if "本栏目暂时没有内容" in html_data:
            return
    try:
        locator = (By.XPATH, "//td[@class='huifont']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1
    # print(cnum)
    url = driver.current_url

    if num != int(cnum):
        if "Paging" not in url:
            s = "?Paging=%d" % (num) if num > 1 else "?Paging=1"
            url = url + s
        elif num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        driver.get(url)
        try:
            locator = (By.XPATH, "(//tr[@height='25']/td/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            # print('刷新一下，继续')
            driver.refresh()
            locator = (By.XPATH, "(//tr[@height='25']/td/a)[1][string()!='%s']" % val)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))



    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("table", cellspacing='3')

    trs = table.find_all("tr", height="25")
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
        td = tr.find("font", color="#000000").text.strip()

        link = "http://www.lssggzy.com" + link.strip()

        tmp = [title, td, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2(driver):
    url = driver.current_url
    if ("http://www.lssggzy.com/lsweb/jyxx/071002/071002008" in url) or ("http://www.lssggzy.com/lsweb/jyxx/071002/071002009" in url):
        locator = (By.XPATH, "(//tr[@height='25']/td/a)[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        try:
            locator = (By.XPATH, "//td[@class='huifont']")
            str = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator)).text
            num = int(re.findall(r'/(\d+)', str)[0])
        except:
            num = 1
        driver.quit()
        return num

    else:
        global num_list
        num_list = []
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        uls = soup.find_all('td', class_='LeftMenuJsgc')
        num = len(uls)
        cnum = 0
        list_1 = []
        for i in range(1, int(num)+1):
            locator = (By.XPATH, "(//font[@class='currentpostionfont'])[last()]")
            val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
            driver.find_element_by_xpath("(//td[@class='LeftMenuJsgc'])[{}]".format(i)).click()
            try:
                locator = (By.XPATH, "(//font[@class='currentpostionfont'])[last()][string()!='%s']" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                time.sleep(2)

            try:
                locator = (By.XPATH, "//td[@class='huifont']")
                str = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator)).text
                num = int(re.findall(r'/(\d+)', str)[0])
            except:
                html_data = driver.page_source
                if "本栏目暂时没有内容" in html_data:
                    num = 1
                else:
                    num = 1
            cnum += num
            list_1.append(num)



        for i in range(1, len(list_1) + 1):
            b = sum(list_1[:i])
            num_list.append(b)

        driver.quit()
        return cnum



def f3(driver, url):
    driver.get(url)

    locator = (By.CLASS_NAME, "top-banner")

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

    div = soup.find('table', style="overflow:hidden")

    div = div.find_all('tr')

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001001/071001001001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_biangen_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001002/071001002001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zishenjieguo_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001003/071001003001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiaohx_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001004/071001004001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001005/071001005001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_xiaoer_zhaobiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001006/071001006001/071001006001001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_xiaoer_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001006/071001006002/071001006002001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_xiaoer_zhongbiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071001/071001006/071001006003/071001006003001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_zhaobiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002002/071002002001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_biangen_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002003/071002003001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiaohx_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002007/071002007001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002005/071002005001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_yucai_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002001/071002001001/",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_xieyi_zhaobiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002008/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_xieyi_zhongbiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071002/071002009/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_zhaobiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qsydw_zhongbiao_gg",
     "http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003001/",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def get_profile():
    path1 = join(dirname(__file__), 'profile')
    with open(path1, 'r') as f:
        p = f.read()

    return p


def get_conp(txt):
    x = get_profile() + ',' + txt
    arr = x.split(',')
    return arr


if gg_existed(conp=get_conp(_name_)):
    CDC_NUM = 5
else:
    CDC_NUM = 100000



def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省丽水市",**args)

    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","lishui"],cdc_total=None)



    # driver=webdriver.Chrome()
    # url="http://www.lssggzy.com/lsweb/jyxx/071001/071001001/071001001001/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(13, 16):
    #     df=f1(driver, i)
    #     print(df)
