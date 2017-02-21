#coding=utf-8
from selenium import webdriver
import time
import sys
from bs4 import BeautifulSoup
sys.path.append("../untitled")
import AllNewsLinks as SS
import mysql
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# driver = webdriver.PhantomJS(executable_path='d:\phantomjs-2.1.1-windows\gbin\phantomjs.exe')
# # driver.get("http://pythonscraping.com/page/javascript/ajaxDemo.html")
# driver.get("http://data.eastmoney.com/dxf/")
# # time.sleep(3)
# print driver.find_element_by_id('month_3').text
# driver.close()
class XSGJJ(SS.ScrawlSite):
    def click_button(self):
        driver = webdriver.PhantomJS(executable_path='d:\phantomjs-2.1.1-windows\gbin\phantomjs.exe')
        # driver.get("http://pythonscraping.com/page/javascript/ajaxDemo.html")
        driver.get(self.url)

        # element = driver.find_element_by_id('month_3')
        # element.click()
        # element.send_keys(Keys.RETURN)
        # driver.find_element(By.LINK_TEXT, "十月份").find_element(By.XPATH,"..").click()
        # element = driver.find_element(By.LINK_TEXT,"十月份").click()
        element = driver.find_element(By.LINK_TEXT, "九月份").click()

        # driver.execute_script("arguments[0].click()", element)

        time.sleep(5)
        pageSource = driver.page_source
        contentbox=driver.find_element(By.XPATH, "//div[@id='table_listcontent']")
        print contentbox.text
        driver.close()
        # print pageSource
        return
        self.soup = BeautifulSoup(pageSource)
        self.FindNewsLinks()

    def FindNewsLinks(self):
        try:
            print "soup:",self.soup
            div = self.soup.find(id='table_listcontent')

            print div
            tr = div.find_all(name='tr')
            print 'tr: ',tr
            for item in tr:
                text = item.find_all(name='td')
                print text
                # for each_item in text:
                #     # print text[0]
                #     print each_item.text.strip()
        except StandardError, e:
            print e

    def gg(self):
        # ret = self.GetSiteContent()
        self.click_button()
def main():
    jj = XSGJJ(url = "http://data.eastmoney.com/dxf/",tablename = "XXX", n = 2)
    jj.gg()

if __name__ == '__main__':
    main()