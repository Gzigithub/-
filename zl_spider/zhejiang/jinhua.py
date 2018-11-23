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
from zhulong.util.etl import gg_meta,gg_html


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


from zhulong.util.etl import add_info,est_meta,est_html,est_tbs,gg_existed


_name_="jinhua"



num_list = []



def f1_data(driver, num, url_1, url_2, url_3):
    url = driver.current_url
    if url_1.rsplit('/', maxsplit=1)[0] in url:
        if num_list[0] < num <= num_list[0]+num_list[1]:
            driver.get(url_2)
            num = num - num_list[0]
        elif num > num_list[0]+num_list[1]:
            driver.get(url_3)
            num = num - (num_list[0]+num_list[1])
        else:
            pass
    elif url_2.rsplit('/', maxsplit=1)[0] in url:
        if num_list[0] < num <= num_list[0]+num_list[1]:
            num = num - num_list[0]
        elif num > num_list[0]+num_list[1]:
            driver.get(url_3)
            num = num - (num_list[0]+num_list[1])
        else:
            driver.get(url_1)
    elif url_3.rsplit('/', maxsplit=1)[0] in url:
        if num_list[0] < num <= num_list[0]+num_list[1]:
            driver.get(url_2)
            num = num - num_list[0]
        elif num > num_list[0]+num_list[1]:
            num = num - (num_list[0]+num_list[1])
        else:
            driver.get(url_1)

    return num



def f1(driver, num):
    # global num_list
    url = driver.current_url
    url_1 = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    url_2 = "http://www.jhztb.gov.cn/jhztb/jsgcgcjszbgg/index.htm"
    url_3 = "http://www.jhztb.gov.cn/jhztb/jsgcjhszbgg/index.htm"
    url_4 = "http://www.jhztb.gov.cn/jhztb/gcjyzbjg/index.htm"
    url_5 = "http://www.jhztb.gov.cn/jhztb/jsgcgcjspbjg/index.htm"
    url_6 = "http://www.jhztb.gov.cn/jhztb/jsgcjhspbjg/index.htm"
    url_7 = "http://www.jhztb.gov.cn/jhztb/gcjyzbzy/index.htm"
    url_8 = "http://www.jhztb.gov.cn/jhztb/jsgcgcjszbjg/index.htm"
    url_9 = "http://www.jhztb.gov.cn/jhztb/jsgcjhszbjg/index.htm"
    url_a = url_1.rsplit('/', maxsplit=1)[0]
    url_b = url_2.rsplit('/', maxsplit=1)[0]
    url_c = url_3.rsplit('/', maxsplit=1)[0]
    url_d = url_4.rsplit('/', maxsplit=1)[0]
    url_e = url_5.rsplit('/', maxsplit=1)[0]
    url_f = url_6.rsplit('/', maxsplit=1)[0]
    url_g = url_7.rsplit('/', maxsplit=1)[0]
    url_h = url_8.rsplit('/', maxsplit=1)[0]
    url_i = url_9.rsplit('/', maxsplit=1)[0]
    if (url_a in url) or (url_b in url) or (url_c in url):
        num = f1_data(driver, num, url_1, url_2, url_3)

    elif (url_d in url) or (url_e in url) or (url_f in url):
        num = f1_data(driver, num, url_4, url_5, url_6)

    elif (url_g in url) or (url_h in url) or (url_i in url):
        num = f1_data(driver, num, url_7, url_8, url_9)


    # 判断是否是第一次爬取，如果是增量更新,只获取前5页
    if num > CDC_NUM:
        return

    locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1]")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    try:
        locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', str)[0]
    except:
        cnum = 1
    # print(cnum)
    url = driver.current_url

    if num != int(cnum):
        if "http://www.jhztb.gov.cn/platform/project/notice" in url:
            if "type" in url:
                s = "page=%d" % (num-1) if num > 1 else "page=0"
                url = re.sub("type=.*", s, url)
            elif num == 1:
                url = re.sub("page=[0-9]*", "page=0", url)
            else:
                s = "page=%d" % (num-1) if num > 1 else "page=0"
                url = re.sub("page=[0-9]*", s, url)
                # print(cnum)
            driver.get(url)
            try:
                locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

        else:
            if "index.htm" in url:
                s = "index_%d" % (num) if num > 1 else "index_1"
                url = re.sub("index", s, url)
            elif num == 1:
                url = re.sub("index_[0-9]*", "index_1", url)
            else:
                s = "index_%d" % (num) if num > 1 else "index_1"
                url = re.sub("index_[0-9]*", s, url)
                # print(cnum)
            driver.get(url)
            try:
                locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
            except:
                driver.refresh()
                locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1][string()!='%s']" % val)
                WebDriverWait(driver, 3).until(EC.presence_of_element_located(locator))

    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    table = soup.find("div", class_='Right-Border floatL')

    trs = table.find_all("dt")
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
        td = tr.find("span").text.strip()
        span = re.findall(r'\[(.*)\]', td)[0]

        if "http://www.jhztb.gov.cn/platform/project/notice" in url:
            link = "http://www.jhztb.gov.cn/platform/project/notice/" + link.strip()
        else:
            link = "http://www.jhztb.gov.cn" + link.strip()

        tmp = [title, span, link]
        data.append(tmp)


    df = pd.DataFrame(data)
    df['info'] = None
    return df



def f2_data(driver):
    locator = (By.XPATH, "(//div[@class='Right-Border floatL']/dl/dt/a)[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        locator = (By.XPATH, "//div[@class='Page-bg floatL']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/(\d+)', str)[0]
    except:
        num = 1

    return int(num)




def f2(driver):
    global num_list
    num_list = []
    url = driver.current_url
    if "http://www.jhztb.gov.cn/jhztb/gcjyysgs/" in url:
        num_1 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcgcjszbgg/index.htm")
        num_2 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcjhszbgg/index.htm")
        num_3 = f2_data(driver)

        num_list.append(num_1)
        num_list.append(num_2)
        num_list.append(num_3)

        num = num_1+num_2+num_3
        # driver.close()
        driver.quit()
        return int(num)
    elif "http://www.jhztb.gov.cn/jhztb/gcjyzbjg/" in url:
        num_1 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcgcjspbjg/index.htm")
        num_2 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcjhspbjg/index.htm")
        num_3 = f2_data(driver)
        num_list.append(num_1)
        num_list.append(num_2)
        num_list.append(num_3)

        num = num_1+num_2+num_3
        # driver.close()
        driver.quit()
        return int(num)
    elif "http://www.jhztb.gov.cn/jhztb/gcjyzbzy/" in url:
        num_1 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcgcjszbjg/index.htm")
        num_2 = f2_data(driver)
        driver.get("http://www.jhztb.gov.cn/jhztb/jsgcjhszbjg/index.htm")
        num_3 = f2_data(driver)
        num_list.append(num_1)
        num_list.append(num_2)
        num_list.append(num_3)
        num = num_1+num_2+num_3
        # driver.close()
        driver.quit()
        return int(num)

    else:
        num = f2_data(driver)
        driver.quit()
        return int(num)



def f3(driver, url):
    driver.get(url)
    try:
        locator = (By.CLASS_NAME, "Head")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
    except:
        html_data = driver.page_source
        if "系统发生内部错误" in html_data:
            return

    locator = (By.CLASS_NAME, "Head")
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

    div = soup.find('div', class_='content-Border floatL')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["gcjs_zhongbiaohx_gg",
     "http://www.jhztb.gov.cn/jhztb/gcjyzbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg",
     "http://www.jhztb.gov.cn/jhztb/gcjyzbzy/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["zfcg_yucai_gg",
     "http://www.jhztb.gov.cn/jhztb/zfcgggyg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg",
     "http://www.jhztb.gov.cn/jhztb/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_gg",
     "http://www.jhztb.gov.cn/jhztb/zfcgzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhongbiao_gg",
     "http://www.jhztb.gov.cn/jhztb/zfcgzbhxgs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_quxian_zhaobiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/area.jsp?type=tenderBulletin&area=&page=0",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_quxian_zhongbiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=winBidBulletin&area=&type=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_quxian_zhongbiaohx_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=winCandidateBulletin&area=&type=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_quxian_zhaobiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=caiGouGGZFCG&area=&type=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_quxian_zhongbiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=zhongBiaoResultZFCG&area=&type=2",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_quxian_zhaobiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=OTHER_TRADE_PUB_INFO&area=&type=5",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_quxian_zhongbiao_gg",
     "http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=OTHER_TRADE_RESULT_INFO&area=&type=5",
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
    est_meta(conp,data=data,diqu="浙江省金华市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","jinhua"],cdc_total=None)


    # driver=webdriver.Chrome()
    # url="http://www.jhztb.gov.cn/platform/project/notice/list.jsp?key=OTHER_TRADE_RESULT_INFO&area=&type=5"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # # driver = webdriver.Chrome()
    # # url = "http://www.jhztb.gov.cn/jhztb/gcjyysgs/index.htm"
    # # driver.get(url)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)