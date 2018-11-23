import lxml
import time

from lxml import etree
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


driver=webdriver.Chrome()
url="http://www.lssggzy.com/lsweb/infodetail/?infoid=53b03655-1269-41c6-bc2e-b16ca508d3de&categoryNum=071001002008"
driver.get(url)
html = driver.page_source

tree=etree.HTML(html)
div=tree.xpath('//td[@class="s-mid-content-title"]')[0]
div_str=etree.tostring(div).decode('gbk')



print(div_str)