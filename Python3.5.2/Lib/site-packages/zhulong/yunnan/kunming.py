import time
from collections import OrderedDict

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


from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg, add_info

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_='kunming'


def f1(driver,num):
    locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url=driver.current_url
    try:
        cnum = driver.find_element_by_xpath('//span[@id="lblAjax_PageIndex"]').text
    except:
        cnum=1

    if cnum == '':cnum=1
    if int(cnum) != num:
        val = driver.find_element_by_xpath('//div[@class="zb_from"]/table/tbody/tr[2]/td[3]').text

        input_page = driver.find_element_by_xpath('//div[@class="pager"]/table/tbody/tr/td[1]/input')
        input_page.clear()
        input_page.send_keys(num, Keys.ENTER)

        locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div = soup.find('div', class_='zb_from').find('table')
    trs = div.find_all('tr')
    data = []

    for i in range(1, len(trs)):
        tr = trs[i]
        tds = tr.find_all('td')
        href = tds[2].a['href']
        name = tds[2].a.get_text()
        index_num = tds[1].get_text()
        ggstart_time = tds[3].get_text()

        if 'http' in href:
            href = href
        else:
            href = 'https://www.kmggzy.com/Jyweb/' + href
        if re.findall('SubType2=1$',url) or re.findall('SubType2=12$',url):

            ggend_time=tds[4].get_text()
            tmp = [index_num, name, href, ggstart_time, ggend_time]
        else:
            tmp = [index_num, name, href, ggstart_time]

        data.append(tmp)

    df=pd.DataFrame(data=data)
    df['info']=None
    return df



def f2(driver):
    locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    try:
        page = driver.find_element_by_xpath('//span[@id="lblAjax_TotalPageCount"]').text
        total = int(page)
    except:
        total=1
    if total=='': total=1
    driver.quit()
    return total


def chang_address_f1(f,i):
    def wrap(*krg):
        driver=krg[0]
        num=krg[1]
        url = driver.current_url
        if re.findall('SubType2=27$', url):
            locator = (By.XPATH, '//*[@id="title11"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        else:
            locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        ctext = driver.find_element_by_xpath('//a[@class="on"]').text.strip()


        if int(i) != 1 and ctext == '昆明市':

            if re.findall('SubType2=27',url):
                val='wushuju'
            else:
                val = driver.find_element_by_xpath('//div[@class="zb_from"]/table/tbody/tr[2]/td[3]').text

            driver.find_element_by_xpath('//div[@class="title3"]/ul/li[{}]/a'.format(i)).click()
            locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        return f(*krg)
    return wrap
def chang_address_f2(f,i):
    def wrap(*krg):
        driver=krg[0]
        url = driver.current_url
        if re.findall('SubType2=27$', url):
            locator = (By.XPATH, '//*[@id="title11"]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        else:
            locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3]')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))


        if int(i) != 1 :

            if re.findall('SubType2=27$',url):
                val='wushuju'
            else:
                val = driver.find_element_by_xpath('//div[@class="zb_from"]/table/tbody/tr[2]/td[3]').text

            driver.find_element_by_xpath('//div[@class="title3"]/ul/li[{}]/a'.format(i)).click()
            locator = (By.XPATH, '//div[@class="zb_from"]/table/tbody/tr[2]/td[3][not(contains(string(),"%s"))]' % val)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

        return f(*krg)
    return wrap


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//table[@class="TableCss1"]  |//div[@class="tableStyle"] |'
                         ' //div[@class="zb_content"]')

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

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
    div = soup.find('table',class_='TableCss1')
    if div == None:
        div = soup.find('div', class_="tableStyle")
        if div == None:
            div=soup.find('div',class_='zb_content')

    return div







def get_data():
    data = []

    ggtype1=OrderedDict([('zhongbiaohx', '24'), ('zhongbiao', '11'), ('liubiao', '5'),('fuhejieguo', '31')])
    ggtype2=OrderedDict([('zhongbiao', '14'),  ('liubiao', '28'),('fuhejieguo', '32')])
    ggtype3=OrderedDict([('zhongbiao', '21'),  ('zhongbiao', '23')])

    adtype1 = OrderedDict([('昆明市', '1'), ("东川区", "2"), ("安宁市", "3"), ("晋宁县", "4"), ("富民县", "5"),
                           ('禄劝县', '6'), ('宜良县', '7'), ('石林县', '8'), ('嵩明县', '9'), ('寻缅县', '10'),
                           ('滇中新区', '11'), ('空港经济区', '12')])

    ####gcjs
    for w1 in adtype1.keys():
        href = "https://www.kmggzy.com/Jyweb/ZBGGList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2=1"
        tmp = ["gcjs_zhaobiao_diqu%s_gg" % adtype1[w1], href,
               ["index_num", "name", "href", "ggstart_time", "ggend_time", "info"],
               chang_address_f1(add_info(f1, {"diqu": w1}),adtype1[w1]), chang_address_f2(f2,adtype1[w1])]
        data.append(tmp)

    for g1 in ggtype1.keys():
        for w1 in adtype1.keys():
            href = "https://www.kmggzy.com/Jyweb/PBJGGSList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=1&SubType2={}".format(ggtype1[g1])
            tmp = ["gcjs_%s_diqu%s_gg" %(g1,adtype1[w1]), href,
                   ["index_num", "name", "href", "ggstart_time","info"],
                   chang_address_f1(add_info(f1, {"diqu": w1}),adtype1[w1]), chang_address_f2(f2,adtype1[w1])]
            data.append(tmp)

    ####zfcg
    for w1 in adtype1.keys():
        href = "https://www.kmggzy.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2=12"
        tmp = ["zfcg_zhaobiao_diqu%s_gg" % adtype1[w1], href,
               ["index_num", "name", "href", "ggstart_time", "ggend_time", "info"],
               chang_address_f1(add_info(f1, {"diqu": w1}),adtype1[w1]), chang_address_f2(f2,adtype1[w1])]
        data.append(tmp)

    for g2 in ggtype2.keys():
        for w1 in adtype1.keys():
            href = "https://www.kmggzy.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=2&SubType2={}".format(ggtype2[g2])
            tmp = ["zfcg_%s_diqu%s_gg" %(g2,adtype1[w1]), href,
                   ["index_num", "name", "href", "ggstart_time","info"],
                   chang_address_f1(add_info(f1, {"diqu": w1}),adtype1[w1]), chang_address_f2(f2,adtype1[w1])]
            data.append(tmp)
    ##qsy
    for g3 in ggtype3.keys():
        for w1 in adtype1.keys():
            href = "https://www.kmggzy.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=5&SubType2={}".format(ggtype3[g3])
            tmp = ["qsy_%s_diqu%s_gg" %(g3,adtype1[w1]), href,
                   ["index_num", "name", "href", "ggstart_time","info"],
                   chang_address_f1(add_info(f1, {"diqu": w1}),adtype1[w1]), chang_address_f2(f2,adtype1[w1])]
            data.append(tmp)

    href='https://www.kmggzy.com/Jyweb/JYXTXXList.aspx?Type=%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF&SubType=5&SubType2=27'
    db_list=["index_num", "name", "href", "ggstart_time","info"]
    data.append(['qsy_liubiao_diqu5_gg',href,db_list,chang_address_f1(add_info(f1, {"diqu": '富民县'}),5), chang_address_f2(f2,5)])
    data.append(['qsy_liubiao_diqu7_gg',href,db_list,chang_address_f1(add_info(f1, {"diqu": '富民县'}),7), chang_address_f2(f2,7)])
    data.append(['qsy_liubiao_diqu8_gg',href,db_list,chang_address_f1(add_info(f1, {"diqu": '富民县'}),8), chang_address_f2(f2,8)])
    data.append(['qsy_liubiao_diqu9_gg',href,db_list,chang_address_f1(add_info(f1, {"diqu": '富民县'}),9), chang_address_f2(f2,9)])
    data.append(['qsy_liubiao_diqu10_gg',href,db_list,chang_address_f1(add_info(f1, {"diqu": '富民县'}),10), chang_address_f2(f2,10)])

    remove_arr = [ 'zfcg_fuhejieguo_diqu10_gg','zfcg_fuhejieguo_diqu11_gg','zfcg_fuhejieguo_diqu12_gg',
        'qsy_zhaobiao_diqu3_gg','qsy_zhaobiao_diqu4_gg','qsy_zhaobiao_diqu11_gg','qsy_zhaobiao_diqu6_gg','qsy_zhaobiao_diqu12_gg',
         'qsy_zhongbiao_diqu3_gg','qsy_zhongbiao_diqu4_gg','qsy_zhongbiao_diqu6_gg','qsy_zhongbiao_diqu11_gg','qsy_zhongbiao_diqu12_gg']

    data1 = data.copy()
    for w in data:
        if w[0] in remove_arr: data1.remove(w)

    return data1


data=get_data()


def work(conp,**args):
    est_meta(conp,data=data,diqu="云南省昆明市",**args)
    est_html(conp,f=f3,**args)


if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","yunnan","kunming"]

    work(conp=conp,num=10,cdc_total=5)