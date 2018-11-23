import pandas as pd
import re

from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
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


_name_="ningbo"


def f1(driver, num):
    url = driver.current_url
    if "http://www.bidding.gov.cn/" not in url:
        tmp = get_data(driver, num)

        df = pd.DataFrame(data=tmp)
        df['info'] = None
        return df

    if 'index.htm' in url:
        url = re.sub('index.htm', 'index_1.htm', url)
        driver.get(url)
    locator = (By.XPATH, "//div[@class='c1-body']/li[1]/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    locator = (By.XPATH, "//div[@class='pg-3']/div")
    str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
    cnum = re.findall(r'(\d+)/', str)[0]
    if num != int(cnum):
        if num == 1:
            url = re.sub("index_[0-9]*", "index_1", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index_1"
            url = re.sub("index_[0-9]*", s, url)

        driver.get(url)

        try:
            locator = (By.XPATH, "//div[@class='c1-body']/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        except:
            driver.refresh()
            locator = (By.XPATH, "//div[@class='c1-body']/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))


    page = driver.page_source

    soup = BeautifulSoup(page, 'lxml')

    div= soup.find("div", class_='c1-body')

    trs = div.find_all("li")
    data = []
    for tr in trs:
        a = tr.find("a")
        try:
            link = a["href"]
        except:
            continue
        span = tr.find("span").text

        tmp = [a["title"].strip(), span.strip(), "http://www.bidding.gov.cn"+link.strip()]
        data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def get_data(driver, num):
    url = driver.current_url
    if "http://www.nbuci.com/Newsinfo/list.aspx?" in url:
        locator = (By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_rpLists_ctl00_hyLink']")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        locator = (By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_bottomfy_CurPage']")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        if num != int(cnum):
            driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_bottomfy_TextBoxGoto"]').clear()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_bottomfy_TextBoxGoto"]').send_keys(num, Keys.ENTER)
            # driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_bottomfy_ButtonGo"]').click()
            # print(url)

            locator = (By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_rpLists_ctl00_hyLink'][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find("table", id='ctl00_ContentPlaceHolder1_TablerpLists')

        trs = div.find_all("table")
        data = []
        for tr in trs:

            a = tr.find('a')
            title = a['title']
            links = a['href']
            link = re.sub(r'\.\./', 'http://www.nbuci.com/', links)
            date = tr.find('td', width="20%")
            tmp = [title.strip(), date.text.strip(), link]
            data.append(tmp)
            # print(tmp)
        return data

    elif 'http://www.nbjttz.com/ztzl/cggs/' in url:
        locator = (By.XPATH, "(//a[@class='style_blue12'])[1]")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        locator = (By.XPATH, "//table[@width='97%']//td[@align='center']/div")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+)/', cnum)[0]

        if num != int(cnum):
            if "index.jhtml" in url:
                s = "index_%d.jhtml" % (num) if num > 1 else "index_1.jhtml"
                url = re.sub("index.jhtml", s, url)
            elif num == 1:
                url = re.sub("index_[0-9]*", "index_1", url)
            else:
                s = "index_%d" % (num) if num > 1 else "index_1"
                url = re.sub("index_[0-9]*", s, url)
                # print(cnum)
            driver.get(url)

            locator = (By.XPATH, "(//a[@class='style_blue12'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find("table", class_='con_list')

        trs = div.find_all("tr")
        data = []
        for tr in trs:
            a = tr.find('a')
            title = a['title']
            link = a['href']
            dates = tr.find('td', width="12%").text.strip()
            date = re.findall(r'\[(.*)\]', dates)[0]
            tmp = [title.strip(), date, "http://www.nbjttz.com"+link]

            data.append(tmp)
            # print(tmp)
        return data

    elif 'http://www.ndig.com.cn/cat/' in url:
        locator = (By.XPATH, "//*[@id='newslist']/li[1]/a")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        locator = (By.XPATH, "//td[@id='pagelist']")
        cnmm = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        cnum = re.findall(r'(\d+) /', cnmm)[0]

        if num != int(cnum):
            driver.execute_script('javascript:showNews({})'.format(12*(num-1)))
            # s1 = Select(driver.find_element_by_xpath('//select[@class="pager"]'))
            # s1.select_by_value("%d" % num)
            locator = (By.XPATH, "//*[@id='newslist']/li[1]/a[string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')
        div = soup.find("ul", id='newslist')
        trs = div.find_all("li")
        data = []
        for tr in trs:
            a = tr.find('a')
            title = a.text
            link = a['href']
            date = tr.find('span', class_="time").text.strip()
            tmp = [title.strip(), date, "http://www.ndig.com.cn"+link]
            data.append(tmp)
        return data


    elif 'http://www.nbmetro.com/index.php?' in url:
        locator = (By.XPATH, "(//p[@class='fl'])[1]")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        locator = (By.XPATH, "//a[@class='active']")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

        if num != int(cnum):
            url = url.rsplit('/', maxsplit=1)[0] + '/{}'.format(num)
            driver.get(url)

            locator = (By.XPATH, "(//p[@class='fl'])[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find("ul", class_='about-list f-cb')

        trs = div.find_all("li")
        data = []
        for tr in trs:
            a = tr.find('a')
            title = a.text
            link = a['href']
            date = tr.find('p', class_="fr").text.strip()
            tmp = [title.strip(), date, "http://www.nbmetro.com/"+link]

            data.append(tmp)
            # print(tmp)
        return data

    elif 'http://www.nbgz.gov.cn/col' in url:
        locator = (By.XPATH, "//ul[@class='list-content']/li[1]")
        val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

        locator = (By.XPATH, "//span[@class='default_pgEndRecord']")
        page_all = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        page_all = int(page_all)
        if page_all/15 == int(page_all/15):
            cnum = int(page_all/15)
        else:
            cnum = int(page_all/15) + 1


        if num != int(cnum):

            time.sleep(1)
            locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).clear()
            locator = (By.XPATH, "//input[@class='default_pgCurrentPage']")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).send_keys(num, Keys.ENTER)
            locator = (By.XPATH, "//ul[@class='list-content']/li[1][string()!='%s']" % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        page = driver.page_source

        soup = BeautifulSoup(page, 'lxml')

        div = soup.find("ul", class_='list-content')

        trs = div.find_all("li")
        data = []
        for tr in trs:
            a = tr.find('a')
            title = a.text
            link = a['href']
            date = tr.find('p').text.strip()
            tmp = [title.strip(), date, "http://www.nbgz.gov.cn"+link]

            data.append(tmp)
            # print(tmp)
        return data



def f2(driver):
    url = driver.current_url
    if "http://www.nbuci.com/Newsinfo/list.aspx?" in url:
        locator = (By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_rpLists_ctl00_hyLink']")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//*[@id='ctl00_ContentPlaceHolder1_bottomfy_SumPage']")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = int(str)

    elif 'http://www.nbjttz.com/ztzl/cggs/' in url:
        locator = (By.XPATH, "(//a[@class='style_blue12'])[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//table[@width='97%']//td[@align='center']/div")
        cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/(\d+)', cnum)[0]

    elif 'http://www.ndig.com.cn/' in url:
        locator = (By.XPATH, "//*[@id='newslist']/li[1]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//td[@id='pagelist']")
        cnmm = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/ (\d+)', cnmm)[0]


    elif 'http://www.nbmetro.com/index.php?' in url:
        locator = (By.XPATH, "(//p[@class='fl'])[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//div[@class='page']/a[11]")
        cnmm = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'(\d+)', cnmm)[0]

    elif 'http://www.nbgz.gov.cn/col' in url:
        locator = (By.XPATH, "//ul[@class='list-content']/li[1]")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        locator = (By.XPATH, "//span[@class='default_pgTotalPage']")
        cnmm = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        num = int(cnmm)

    else:
        locator = (By.XPATH, "//div[@class='c1-body']/li[1]/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//div[@class='pg-3']/div")
        str = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text
        num = re.findall(r'/(\d+)', str)[0]


    driver.quit()
    return int(num)

def f3_1(driver, url):
    driver.get(url)
    locator = (By.CLASS_NAME, "largefont")

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

    table = soup.find('table', attrs={'width':'84%', 'height':'357'})
    div = table.find('tbody')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div

def f3_2(driver, url):
    driver.get(url)
    locator = (By.CLASS_NAME, "search_text")

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

    try:
        html_data = driver.page_source
        if "详见链接" in html_data:
            locator = (By.XPATH, "//*[@id='content']")
            source = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
            link = re.findall(r'(http.*)', source)[0].strip()
            driver.get(link)
            locator = (By.CLASS_NAME, "siteToolbar")
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
            div = soup.find('div', class_='frameNews')
            # div=div.find_all('div',class_='ewb-article')[0]
            return div

    except:
        pass

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

    div = soup.find('div', id='content')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


def f3_3(driver, url):
    driver.get(url)
    locator = (By.CLASS_NAME, "main")

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

    div = soup.find('div', class_='wordsbox')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


def f3_4(driver, url):
    driver.get(url)
    locator = (By.CLASS_NAME, "con")

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

    div = soup.find('div', class_='news-content-text-wrap')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div

def f3_5(driver, url):
    driver.get(url)
    locator = (By.CLASS_NAME, "Wrap")

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

    div = soup.find('div', id='zoom')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div


def f3(driver, url):
    if "http://www.nbuci.com/" in url:
        df = f3_1(driver, url)
        return df
    elif "http://www.nbjttz.com/" in url:
        df = f3_2(driver, url)
        return df
    elif "http://www.ndig.com.cn/" in url:
        df = f3_3(driver, url)
        return df
    elif "http://www.nbmetro.com/" in url:
        df = f3_4(driver, url)
        return df
    elif "http://www.nbgz.gov.cn/" in url:
        df = f3_5(driver, url)
        return df
    driver.get(url)
    locator = (By.CLASS_NAME, "siteToolbar")

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

    div = soup.find('div', class_='frameNews')
    # div=div.find_all('div',class_='ewb-article')[0]

    return div



data = [
    ["gcjs_zhaobiao_gg","http://www.bidding.gov.cn/gcjszbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiaohx_gg", "http://www.bidding.gov.cn/gcjsyzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["gcjs_zhongbiao_gg", "http://www.bidding.gov.cn/gcjszbgg1/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["zfcg_zhaobiao_gg", "http://www.bidding.gov.cn/zfcgcggg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg", "http://www.bidding.gov.cn/zfcggggg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_gg", "http://www.bidding.gov.cn/zfcgcgyg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["lishi_zhongbiao_gg", "http://www.bidding.gov.cn/lszbggcx/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qsydw_zhaobiao_gg", "http://www.bidding.gov.cn/clsbzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhongbiaohx_gg", "http://www.bidding.gov.cn/jsgcclsbzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qsydw_zhongbiao_gg", "http://www.bidding.gov.cn/clysbzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qita_zhaobiao_gg", "http://www.bidding.gov.cn/qtjygg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qita_zhongbiaohx_gg", "http://www.bidding.gov.cn/qtjyjggs/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ["qita_zhongbiao_gg", "http://www.bidding.gov.cn/qtzbjg/index.htm",
     ["name", "ggstart_time", "href", "info"],f1,f2],


    ["qita_gc_xinxi_guoqizhaobiao5_gg", "http://www.nbgz.gov.cn/col/col9152/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_gc_jieguo_guoqizhaobiao5_gg", "http://www.nbgz.gov.cn/col/col9153/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_wuzi_xinxi_guoqizhaobiao5_gg", "http://www.nbgz.gov.cn/col/col9154/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_wuzi_jieguo_guoqizhaobiao5_gg", "http://www.nbgz.gov.cn/col/col9155/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_guoqizhaobiao5_gg", "http://www.nbgz.gov.cn/col/col9155/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_zhaobiao_guoqizhaobiao4_gg", "http://www.nbmetro.com/index.php?tender_report/index/1/1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_zhongbiao_guoqizhaobiao4_gg", "http://www.nbmetro.com/index.php?tender_report/index/2/1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_bixuan_guoqizhaobiao4_gg", "http://www.nbmetro.com/index.php?tender_report/index/10/1",
     ["name", "ggstart_time", "href", "info"], f1, f2],


    ["qita_zhaobiao_guoqizhaobiao3_gg", "http://www.ndig.com.cn/cat/cat26/index.html",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_guoqizhaobiao2_gg", "http://www.nbjttz.com/ztzl/cggs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qita_guoqizhaobiao1_gg", "http://www.nbuci.com/Newsinfo/list.aspx?path_id=000000100701082",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="浙江省宁波市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","zhejiang","ningbo"])


    # driver=webdriver.Chrome()
    # url="http://www.nbgz.gov.cn/col/col9153/index.html"
    # driver.get(url)
    # # driver.set_page_load_timeout(2)
    # # driver.set_script_timeout(2)
    # df = f2(driver)
    # print(df)
    # driver=webdriver.Chrome()
    # url="http://www.nbgz.gov.cn/col/col9153/index.html"
    # driver.get(url)
    # d = f3(driver, "http://www.nbmetro.com/tender.php?info/1821")
    # print(d)
    # for i in range(1, 6):
    #     df=f1(driver, i)
    #     print(df)