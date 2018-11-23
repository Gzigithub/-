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
    locator = (By.XPATH, "//table[@height='26']/tbody/tr[2]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # cnum=int(driver.find_element_by_xpath("//span[@class='pageBtnWrap']/span[@class='curr']").text)
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "index.html" in url:
        cnum = 1
        url = re.sub("index_1", "index", url)
    else:
        cnum = int(re.findall("index_(\d+)", url)[0])
    if num != cnum:
        url = driver.current_url
        if num == 1:
            url = re.sub("index_[0-9]*", "index", url)
        elif "index.html" in url:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index", s, url)
        else:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index_(\d+)", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("//table[@height='26']/tbody/tr[2]/td/a").text
        print(url)
        driver.get(url)
        time.sleep(1)
        # print("1111")
        locator = (By.XPATH, '//td[@class="pagerTitle"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall(r'(\d+)/', page_all)[0]
        if int(page) != num:
            locator = (By.XPATH, "//table[@height='26']/tbody/tr[2]/td/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    tb = soup.find("table", height="26", width="100%")
    trs = tb.find_all("tr")
    data = []
    for li in trs[1:]:
        # print(li)
        a = li.find("a")
        # print(a["title"])
        link = "http://zwgk.pingdu.gov.cn" + a["href"]
        span = li.find("td", width="80")
        tmp = [a.text.strip(), span.text.strip(), link]
        data.append(tmp)

        # print(data)
    df = pd.DataFrame(data=data)
    return df




def f2(driver):

    locator = (By.XPATH, '//td[@class="pagerTitle"]')
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
        ["yuzhaobiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3591/index.html",
         ["name", "ggstart_time", "href"]],

        ["zhaobiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3592/index.html",
         ["name", "ggstart_time", "href"]],


        ["zhongbiao_gg","http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3593/index.html",
         ["name", "ggstart_time", "href"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
    for w in data:
        general_template(w[0], w[1], w[2], conp)


if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","pingdu"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://zwgk.pingdu.gov.cn/n3318/n3578/n3590/n3591/index.html"
    # driver.get(url)
    # df = f2(driver)
    # print(df)
    # for i in range(1, 8):
    #     df=f1(driver, i)
    #     print(df)
