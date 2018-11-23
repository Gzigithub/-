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
    # 获取当前页的url
    url = driver.current_url
    html = driver.page_source
    if ("074002003" in url) or ("074001002" in url) or ("074006002" in url) or ("074006001" in url) or ("074006003" in url):
        if ("首页" in html) and ("末页" in html):
            try:
                locator = (By.XPATH, '(//ul[@class="ewb-news-items ewb-build-items"]/li/a)[1]')
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
                data = f1_data(driver, num)
                df = pd.DataFrame(data=data)
                # print(df)
                return df
            except:
                print("err_url:{}".format(url))

    else:
        if "Paging" in url:
            # print(url)
            url_3 = url.rsplit('/', maxsplit=2)[0]
            # print(url_3)
            driver.get(url_3)
        # 获取当前页的url
        # print(url)
        locator = (By.XPATH, '(//h2[@class="wb-colu-tt wb-colu-tt-fs"]/a)[{}]'.format(num))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).click()
        # url_link = driver.find_element_by_xpath('(//td[@class="MoreinfoColor"]/a)[{}]'.format(num)).click()
        # print(url)
        try:
            locator = (By.XPATH, '(//ul[@class="ewb-news-items ewb-build-items"]/li/a)[1]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            html = driver.page_source
            if "本栏目信息正在更新中" in html:
                url_s = driver.current_url
                url_3 = url_s.rsplit('/', maxsplit=2)[0]
                print(url_3)
                driver.get(url_3)
                time.sleep(1)
                return
        page_num = driver.find_element_by_xpath('//span[@class="total-pages"]/strong').text
        # 获取总页数
        page = re.findall('/(\d+)', page_num)[0]
        # print(page)
        data_list = []
        for i in range(int(page) + 1):
            if i == 0:
                continue
            else:
                # print(i)
                df = f1_data(driver, i)
                # print(df)
                data_list.append(df)
        # print(data_list)

        data = []
        for i in data_list:
            for j in i:
                data.append(j)

        df = pd.DataFrame(data=data)
        # print(df)
        return df


def f1_data(driver, i):
    url_i = driver.current_url
    # print(url_i)
    if "Paging" not in url_i:
        # print(url)
        url_2 = url_i.rsplit('/', maxsplit=1)[0]
        # print(url_3)
        url_1 = url_2 + "/?Paging={}".format(i)
        # print(url_1)
        driver.get(url_1)
    cunn = driver.find_element_by_xpath('//span[@class="total-pages"]/strong').text
    # 获取总页数
    cunm = re.findall('(\d+)/', cunn)[0]
    if i != int(cunm):
        url_1 = re.sub(r"(\?Paging=[0-9]*)", "?Paging={}".format(i), url_i)
        val = driver.find_element_by_xpath('(//ul[@class="ewb-news-items ewb-build-items"]/li/a)[1]').text
        # print(url)
        driver.get(url_1)
        locator = (By.XPATH, "(//ul[@class='ewb-news-items ewb-build-items']/li/a)[1][string()!='%s']" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    # print(url_1)
    html_data = driver.page_source
    soup = BeautifulSoup(html_data, 'lxml')
    ul = soup.find("ul", class_="ewb-news-items ewb-build-items")
    lis = ul.find_all("li")
    data = []
    for li in lis:
        # print(li)
        a = li.find("a")

        title = a["title"]
        # print(a["title"])
        link = "http://ggzyjy.linyi.gov.cn" + a["href"]
        span = li.find("span")
        tmp = [title, span.text.strip(), link]
        data.append(tmp)


    return data

    #     cnum=1
    # else:
    #     cnum=int(re.findall("/([0-9]{1,}).html", url)[0])
    # if num!=cnum:
    #     if num==1:
    #         url=re.sub("[0-9]*.html","about.html",url)
    #     else:
    #         s = "%d.html" % (num) if num > 1 else "index.html"
    #         url = re.sub("about[0-9]*.html", s, url)
    #         # print(cnum)
    #     val = driver.find_element_by_xpath("(//div[@class='ewb-info-a']/a)[1]").text
    #     # print(url)
    #     driver.get(url)
    #     time.sleep(2)
    #
    #     locator = (By.XPATH, "(//div[@class='ewb-info-a']/a)[1][string()!='%s']" % val)
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))





def f2(driver):
    """
    返回总页数
    :param driver:
    :return:
    """
    try:
        locator = (By.XPATH, '//span[@class="total-pages"]/strong')
        page_all = WebDriverWait(driver, 1).until(EC.presence_of_element_located(locator)).text
        page = re.findall('/(\d+)', page_all)[0]
    except Exception as e:
        # page_all = driver.find_element_by_xpath("//h2[@class='wb-colu-tt wb-colu-tt-fs']/a/text()")
        html = driver.page_source
        html_data = etree.HTML(html)
        page = html_data.xpath("//h2[@class='wb-colu-tt wb-colu-tt-fs']/a/text()")
        page = len(page)


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
        "num": 15,  # 线程数量

    }
    m = web()
    m.write(**setting)


def work(conp, i=-1):
    data = [

        # ["gcjs_zhaobiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001001/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_biangeng_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001002/",
        #  ["name", "ggstart_time", "href"]],
        # ["gcjs_zhongbiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003003/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["gcjs_zishenjiegou_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003001/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["gcjs_zhongbiaohx_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074001/074001003/074001003002/",
        #  ["name", "ggstart_time", "href"]],
        #
        # ["zfcg_yuzhaobiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002001/",
        #  ["name", "ggstart_time", "href"]],
        # ["zfcg_zhaobiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002002/",
        #  ["name", "ggstart_time", "href"]],
        # ["zfcg_biangeng_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002003/",
        #  ["name", "ggstart_time", "href"]],
        # ["zfcg_zhongbiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074002/074002004/",
        #  ["name", "ggstart_time", "href"]],

        ["qsydw_zhaobiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074006/074006001/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_biangeng_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074006/074006002/?Paging=1",
         ["name", "ggstart_time", "href"]],
        ["qsydw_zhongbiao_gg", "http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074006/074006003/?Paging=1",
         ["name", "ggstart_time", "href"]],
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
    conp=["postgres","since2015","192.168.3.171","shandong","linyi"]

    work(conp=conp)

    # driver=webdriver.Chrome()
    # url="http://ggzyjy.linyi.gov.cn/TPFront/jyxx/074006/074006002/?Paging=1"
    # driver.get(url)
    # # df = f2(driver)
    # # print(df)
    #
    # for i in range(1,3):
    #     df=f1(driver, i)
    #     print(df)
