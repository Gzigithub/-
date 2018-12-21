import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zhulong.util.etl import est_tbs,est_meta,est_html,gg_existed

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hefei.gov.cn/jyxx/002001/002001002/moreinfo_jyxx.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)


_name_='wuhu'



def f1(driver,num):
    url = driver.current_url

    locator = (By.XPATH, '//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


    cnum = re.findall('\/(\d+?).html', url)[0]

    main_url = url.rsplit('/', maxsplit=1)[0]

    if int(cnum) != num:
        val = driver.find_element_by_xpath('//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a').text
        url = main_url + '/' + str(num) + '.html'

        driver.get(url)

        locator = (By.XPATH, '//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a[not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    data = []

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('table', class_='ewb-table')
    tbody = div.find('tbody')
    trs = tbody.find_all('tr')
    for tr in trs:

        tds = tr.find_all('td')
        address = tds[1].span.get_text().strip(']').strip('[')
        href = tds[1].a['href']
        content = tds[1].a['title']
        if '</font>' in content:

            name = re.findall(r'</font>(.+)', content)[0]
        else:

            name = content
        ggstart_time = tds[2].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'http://whsggzy.wuhu.gov.cn' + href

        tmp = [address, name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df['info']=None
    return df


def f2(driver):
    url = driver.current_url
    locator = (By.XPATH, '//table[@class="ewb-table"]/tbody/tr[1]/td[2]/a')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//div[@class="ewb-page"]/ul/li[last()-3]/span').text
        total = re.findall('/(\d+)', page)[0]
        total = int(total)
    except:
        total=1

    driver.quit()
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//div[@class="article-info"]')

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


    div = soup.find('div', class_='con')


    return div

data=[
        #
    ["gcjs_zhaobiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005001/005001001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["gcjs_zhongbiaohx_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005001/005001003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["gcjs_zhongbiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005001/005001004/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["gcjs_liubiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005001/005001005/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ["zfcg_zhaobiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005002/005002001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["zfcg_zhongbiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005002/005002003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["zfcg_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005002/005002004/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ["zfcg_yucai_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005002/005002005/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],


    #
    ["qita_zhaobiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005007/005007001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qita_zhongbiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005007/005007002/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ["qsy_zhaobiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005008/005008001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongbiaohx_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005008/005008003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongbiao_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005008/005008004/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005008/005008005/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ["qita_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005013/1.html", ['address', 'name', 'ggstart_time', 'href', 'info'],
     f1, f2],
    ["qita_gs", "http://whsggzy.wuhu.gov.cn/jyxx/005014/1.html", ['address', 'name', 'ggstart_time', 'href', 'info'],
     f1, f2],


    ["qsy_zhaobiao_shzj_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005009/005009001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongliubiao_shzj_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005009/005009003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ### 此表只有一个数据，无法插入
    ### ["qsy_cgfs_shzj_gg","http://whsggzy.wuhu.gov.cn/jyxx/005009/005009004/1.html",['address',  'status','name', 'ggstart_time', 'href']],

    ["qsy_zhaobiao_gq_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005011/005011001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongbiaohx_gq_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005011/005011003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongbiao_gq_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005011/005011004/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

    ["qsy_zhaobiao_cwfs_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005012/005012001/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],
    ["qsy_zhongliubiao_cwfs_gg", "http://whsggzy.wuhu.gov.cn/jyxx/005012/005012003/1.html",
     ['address', 'name', 'ggstart_time', 'href', 'info'], f1, f2],

]


def work(conp,**args):
    est_meta(conp,data=data,diqu="安徽省芜湖市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","anhui","wuhu"]

    work(conp=conp)