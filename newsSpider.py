#coding=utf-8
#!/usr/bin/python
from time import sleep, ctime
from bs4 import BeautifulSoup
from urllib import urlopen ,urlcleanup
import urllib2
import sys
import re
sys.path.append("../untitled")
import AllNewsLinks as SS
import mysql

# class EM(SS.ScrawlSite):        #东方财富限售股解禁时间表+

class ifengFinance(SS.ScrawlSite):
    def __init__(self,url,dbname,tablename,market,n):
        self.market = market
        self.url = url
        self.dbname = dbname
        self.tablename = tablename
        self.n = n
        self.soup = BeautifulSoup("lxml")
        self.db = mysql.MYSQL(host="192.168.16.84", user="root", pwd="anzl", db=self.dbname)
        self.db.ConnectDB()
    def  FindNewsLinks(self):
        div = self.soup.find(name='table')
        # print div
        tr = div.find_all(name='tr')
        # print 'li: ',li
        for item in tr:
            td = item.find_all(name='td')
            if len(td)==7:
                (stockcode, companyname, appointmentdate, reschedules_1, reschedules_2, reschedules_3, actualdate)\
                = td[0].text.strip(),td[1].text.strip(),td[2].text.strip()[:10],td[3].text.strip()[:10],td[4].text.strip()[:10],\
                  td[5].text.strip()[:10],td[6].text.strip()[:10]
                sqlstr = self.SaveSchedules(self.dbname, self.tablename, stockcode, companyname, appointmentdate, reschedules_1,
                              reschedules_2, reschedules_3, actualdate, self.market)
                self.db.ExecNonQuery(sqlstr)
            # print text
            # for each_item in td:
            #     # print text[0]
            #     print each_item.text.strip()

    def SaveSchedules(self, dbname,tablename,stockcode, companyname, appointmentdate, reschedules_1,reschedules_2,reschedules_3,actualdate,market):

        sqlstr = "insert into `%s`.`%s` (`stockcode`, `companyname`, `appointmentdate`, `reschedules_1`,`reschedules_2`,`reschedules_3`," \
                 "`actualdate`,`market`) values ( '%06d', '%s',str_to_date( '%s','%%Y-%%m-%%d'),str_to_date( '%s','%%Y-%%m-%%d'),str_to_date( '%s','%%Y-%%m-%%d')," \
                 "str_to_date( '%s','%%Y-%%m-%%d'),str_to_date( '%s','%%Y-%%m-%%d'),'%s')" % (dbname, tablename,int(stockcode), companyname, appointmentdate, reschedules_1,reschedules_2,reschedules_3,actualdate,market)
        print stockcode, companyname, appointmentdate, reschedules_1,reschedules_2,reschedules_3,actualdate,market
        return sqlstr

    def gg(self):
        n = 1
        while(n <= self.n):
            if n == 1:
                pass
            else :
                self.url += '&p='+str(n)
                print self.url
            self.GetSiteContent()
            self.FindNewsLinks()
            n += 1
        self.db.conn.commit()

class EM(SS.ScrawlSite):
    def FindNewsLinks(self):
        try:
            div = self.soup.find(id='tablefont')
            # print div
            tr = div.find_all(name='tr')
            # print 'li: ',li
            for item in tr:
                text = item.find_all(name='span')
                # print text
                for each_item in text:
                    # print text[0]
                    print each_item.text.strip()
        except StandardError, e:
            print e
    def gg(self):
        ret = self.GetSiteContent()
        if ret == 1:
            return (None,None,None)
        self.FindNewsLinks()
        # self.SaveNewsLinks()
        # self.db.conn.commit()


def main():
    # em = EM(url = "http://soft-f9.eastmoney.com/soft/gp6.php?code=30034302",tablename = "XXX", n = 2)
    # em.gg()
    ifeng = ifengFinance(url = "http://app.finance.ifeng.com/list/bookinfo_zt.php?t=cyb",dbname='idxdb' ,tablename = "treport",market=3, n = 12)
    ifeng.gg()
if __name__ == '__main__':
    main()
