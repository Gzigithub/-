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


# __conp=["postgres","since2015","192.168.3.171","hunan","zhuzhou"]





def f1(driver, num):
    """
    进行翻页，并获取数据
    :param driver: 已经访问了url
    :param num: 返回的是从第一页一直到最后一页
    :return:
    """
    locator = (By.XPATH, '(//div[@class="ewb-info-a"]/a)[1]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    # 获取当前页的url
    url = driver.current_url
    # print(url)
    if "about.html" in url:
        cnum=1
    else:
        cnum=int(re.findall("/([0-9]{1,}).html", url)[0])
    if num!=cnum:
        if num==1:
            url=re.sub("[0-9]*.html","about.html",url)
        else:
            s = "%d.html" % (num) if num > 1 else "index.html"
            url = re.sub("about[0-9]*.html", s, url)
            # print(cnum)
        val = driver.find_element_by_xpath("(//div[@class='ewb-info-a']/a)[1]").text
        # print(url)
        driver.get(url)
        time.sleep(2)

        locator = (By.XPATH, "(//div[@class='ewb-info-a']/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    ul = soup.find("ul", class_="ewb-info-items")

    lis = ul.find_all("li", class_="ewb-info-item clearfix")
    data = []
    for li in lis:
        a = li.find("a")
        link = "http://www.sdsggzyjyzx.gov.cn" + a["href"]
        span = li.find("span", class_="ewb-date")
        tmp = [a.text.strip(), span.text.strip(), link]
        data.append(tmp)

    df = pd.DataFrame(data=data)
    return df


def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    try:
        locator = (By.XPATH, '//*[@id="index"]')
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        page = re.findall('/(.*)', page_all)[0]
        # print(page)
    except Exception as e:
        page = "1"
    return int(page)


def general_template(tb, url, col, conp):
    m = web()
    setting = {
        "url": url,
        "f1": f1,
        "f2": f2,
        "tb": tb,  # 表名
        "col": col,  # 字段名
        "conp": conp,  # 数据库连接
        "num": 10,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [
        ["zfcg_caigoudongtai_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002001/about.html",
         ["name", "ggstart_time", "href"]],
        ["zfcg_caigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002002/about.html",
         ["name", "ggstart_time", "href"]],
        ["zfcg_biangeng_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002003/about.html",
         ["name", "ggstart_time", "href"]],
        ["zfcg_zhongbiao_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002004/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_yaopincaigou_tongzhi_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001001/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_yaopincaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001002/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_yaopincaigou_geshicaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004001/069004001003/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_haocaicaigou_tongzhi_gg","http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004002/069004002001/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_haocaicaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004002/069004002002/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_yimiaocaigou_tongzhi_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004003/069004003001/about.html",
         ["name", "ggstart_time", "href"]],
        ["ylcg_yimiaocaigou_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069004/069004003/069004003002/about.html",
         ["name", "ggstart_time", "href"]],


        # ["zfcg_caigoudongtai_gg", "http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002001/about.html",
        #  ["tenderPrjName_link", "datagrid-td-rownumber",  "tenderPrjName", "noticeState", "registrationId", "prjbuildCorpName",
        #   "noticeStartDate", "noticeEndDate", "totalInvestment", "platformDataSourceName", "evaluationMethodName"
        #   ]],

        # ["gcjs_fangwu_zhaobiao_gg", "http://www.zzzyjy.cn/016/016001/016001001/1.html",
        #  ["name", "href", "ggstart_time"]],

        # ["gcjs_fangwu_zhongbiaohx_gg", "http://www.zzzyjy.cn/016/016001/016001004/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_fangwu_zhongbiao_gg", "http://www.zzzyjy.cn/016/016001/016001006/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shizheng_zhaobiao_gg", "http://www.zzzyjy.cn/016/016002/016002001/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shizheng_zhongbiaohx_gg", "http://www.zzzyjy.cn/016/016002/016002004/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shizheng_zhongbiao_gg", "http://www.zzzyjy.cn/016/016002/016002006/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_jiaotong_zhaobiao_gg", "http://www.zzzyjy.cn/016/016003/016003001/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_jiaotong_zhongbiaohx_gg", "http://www.zzzyjy.cn/016/016003/016003004/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_jiaotong_zhongbiao_gg", "http://www.zzzyjy.cn/016/016003/016003006/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shuili_zhaobiao_gg", "http://www.zzzyjy.cn/016/016004/016004001/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shuili_zhongbiaohx_gg", "http://www.zzzyjy.cn/016/016004/016004004/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["gcjs_shuili_zhongbiao_gg", "http://www.zzzyjy.cn/016/016004/016004006/1.html",
        #  ["name", "href", "ggstart_time"]],
        #
        # ["zfcg_zhaobiao_gg", "http://www.zzzyjy.cn/017/017001/1.html", ["name", "href", "ggstart_time"]],
        #
        # ["zfcg_zhongbiao_gg", "http://www.zzzyjy.cn/017/017003/1.html", ["name", "href", "ggstart_time"]],
        #
        # ["zfcg_biangen_gg", "http://www.zzzyjy.cn/017/017002/1.html", ["name", "href", "ggstart_time"]],
        #
        # ["zfcg_liubiao_gg", "http://www.zzzyjy.cn/017/017004/1.html", ["name", "href", "ggstart_time"]],

    ]
    if i == -1:
        data = data
    else:
        data = data[i:i + 1]
        print(data)
    for w in data:
        general_template(w[0], w[1], w[2], conp)


# conp = []

if __name__ == '__main__':
    conp=["postgres","since2015","192.168.3.171","shandong","shandong"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://www.sdsggzyjyzx.gov.cn/jyxx/069002/069002001/about.html"
    # driver.get(url)
    # df=f2(driver)
    # print(df)
