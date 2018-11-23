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

from lmfscrap import web


# __conp=["postgres","since2015","192.168.3.171","hunan","changsha"]


# url="https://ggzy.changsha.gov.cn/spweb/CS/TradeCenter/tradeList.do?Deal_Type=Deal_Type2"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


def f1(driver, num):
    locator = (By.XPATH, "(//a[@class='WebList_sub'])[1]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "Paging=" not in url:
        url = url + "?Paging=1"
        driver.get(url)
        cnum = 1
    else:
        cnum = int(re.findall("Paging=(\d+)", url)[0])
    if num != cnum:
        if num == 1:
            url = re.sub("Paging=[0-9]*", "Paging=1", url)
        else:
            s = "Paging=%d" % (num) if num > 1 else "Paging=1"
            url = re.sub("Paging=[0-9]*", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//a[@class='WebList_sub'])[1]").text
        driver.get(url)
        # print("1111")
        locator = (By.XPATH, '//td[@class="huifont"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(r'(\d+)/', page_all)[0]
        if int(page) != num:
            locator = (By.XPATH, "(//a[@class='WebList_sub'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    div = soup.find("div", id='right_table')
    tb = div.find("table", attrs={"width":"98%", "align":"center"})
    trs = tb.find_all("tr", attrs={'height':'30'})
    data = []
    for li in trs:
        # print(li)
        a = li.find("a")
        title = a['title']
        # print(a["title"])
        link = "http://www.taggzyjy.com.cn" + a["href"]
        span = li.find("td", width='80').text.strip()
        date = re.findall(r'\[(.*)\]', span)[0]

        tmp = [title.strip(), date, link]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df




def f2(driver):

    locator = (By.XPATH, '//td[@class="huifont"]')
    page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    page = re.findall(r'/(\d+)', page_all)[0]


    return int(page)



def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,
        "col": col,
        "conp": conp,
        "num": 10,

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["gcjs_zhaobiao_gg","http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075001/075001001/",
         ["name", "ggstart_time", "href"]],

        ["gcjs_biangeng_gg","http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075001/075001003/",
         ["name", "ggstart_time", "href"]],

        ["gcjs_zhongbiao_gg","http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075001/075001002/",
         ["name", "ggstart_time", "href"]],


       ["zfcg_zhaobiao_gg", "http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075002/075002001/",
        ["name", "ggstart_time", "href"]],

       ["zfcg_biangeng_gg", "http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075002/075002003/",
        ["name", "ggstart_time", "href"]],

       ["zfcg_zhongbiao_gg", "http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075002/075002002/",
        ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","feicheng"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.taggzyjy.com.cn/Web_FeiCheng/jyxx/075001/075001001/"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 5):
    #     df=f1(driver, i)
    #     print(df)
