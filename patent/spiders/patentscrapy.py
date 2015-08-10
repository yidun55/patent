#!usr/bin/env python
#coding: utf-8

"""
从专利局官网上爬取各公司的专利信息
"""
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from scrapy import signals
from scrapy import log
import scrapy
import re
import sys
import os
import urllib, urllib2
from patent.items import *

reload(sys)
sys.setdefaultencoding("utf-8")

class patent(BaseSpider):
    # download_delay=2
    name = 'patent22'
    start_urls = ['http://epub.sipo.gov.cn/patentoutline.action']
    allowed_domains=['epub.sipo.gov.cn']
    handle_httpstatus_list = [200,500, 503, 504, 400, 403, 404, 405, 408]
    rawData = {}
    def __inti__(self):
        self.rawData = {"showType":"1",'strWord':"",
            "numSortMethod":"4","strLicenseCode":"",
            "selected":"","numFMGB":"0","numFMSQ":"","numSYXX":"",
            "numWGSQ":"","pageSize":"10","pageNow":"1"}

    def make_requests_from_url(self,url):
        # strWord = "公开（公告）号='CN201310%' or 申请日,公开（公告）日,\
        # 进入国家日期+='2013.10' or 申请号,本国优先权,分案原申请号+='201310%'\
        #  or 申请（专利权）人,发明（设计）人,代理人,优先权,本国优先权,\
        #  分案原申请号,生物保藏,国际申请,国际公布+='%201310%' or \
        #  地址,名称,专利代理机构,摘要+='201310'"
        strWord = "公开（公告）号='CN198509%' or 申请日,公开（公告）日,\
        进入国家日期+='1985.09' or 申请（专利权）人,发明（设计）人,代理人,\
        优先权,本国优先权,分案原申请号,生物保藏,国际申请,国际公布+='%198509%' \
        or 地址,名称,专利代理机构,摘要+='198509'"
        # strWord = "公开（公告）号='CN%s%%' or 申请日,公开（公告）日,\
        # 进入国家日期+='%s' or 申请（专利权）人,发明（设计）人,代理人,\
        # 优先权,本国优先权,分案原申请号,生物保藏,国际申请,国际公布+='%%%s%%' \
        # or 地址,名称,专利代理机构,摘要+='%s'"

        # fInput = []
        # for i in sInput:
        #     fInput.append(strWord %(i, i[0:4]+'.'+i[4:6],i,i))

        data1 = {"showType":"1",'strWord':"",
            "numSortMethod":"4","strLicenseCode":"",
            "selected":"","numFMGB":"0","numFMSQ":"","numSYXX":"",
            "numWGSQ":"","pageSize":"10","pageNow":"1"}
        # for strWord in fInput:
        data1["strWord"] = strWord
        return FormRequest(url,
                    formdata=data1,
                    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.3; en-US; rv:37.0) Gecko/20100101 Firefox/37.0',
                    'Referer':"http://epub.sipo.gov.cn"},
                    callback=self.gettotal,dont_filter=True)

    def gettotal(self, response):
        # print response.body
        # print "i'm end ok"
        sInput = []
        for i in xrange(2015, 2016):
            for j in xrange(06, 10):
                if j<=9:
                    sInput.append(str(i)+"0"+str(j))
                else:
                    sInput.append(str(i)+str(j))

        #for i in xrange(2015, 2016):
        #    for j in xrange(1, 6):
        #       if j<=9:
        #            sInput.append(str(i)+"0"+str(j))
        #        else:
        #            sInput.append(str(i)+str(j))

        strWord = "公开（公告）号='CN%s%%' or 申请日,公开（公告）日,\
        进入国家日期+='%s' or 申请（专利权）人,发明（设计）人,代理人,\
        优先权,本国优先权,分案原申请号,生物保藏,国际申请,国际公布+='%%%s%%' \
        or 地址,名称,专利代理机构,摘要+='%s'"  #00年前所有月份，00年后1到9月

        fInput = []
        for i in sInput:
            fInput.append(strWord %(i, i[0:4]+'.'+i[4:6],i,i))

        # strWord = "公开（公告）号='CN%s%%' or 申请日,公开（公告）日,进入国家日期+='%s' \
        # or 申请号,本国优先权,分案原申请号+='%s%%' or 申请（专利权）人,发明（设计）人,代理人,\
        # 优先权,本国优先权,分案原申请号,生物保藏,国际申请,国际公布+='%%%s%%' or 地址,名称,\
        # 专利代理机构,摘要+='%s'"  #00年后大于9的月份
        # fInput = []
        # for i in sInput:
        #     fInput.append(strWord %(i, i[0:4]+'.'+i[4:6],i,i,i))

        data1 = {"showType":"1",'strWord':"",
            "numSortMethod":"4","strLicenseCode":"",
            "selected":"","numFMGB":"0","numFMSQ":"","numSYXX":"",
            "numWGSQ":"","pageSize":"10","pageNow":"1"}
        url = 'http://epub.sipo.gov.cn/patentoutline.action'
        for strWord in fInput:
            data1["strWord"] = strWord
            yield FormRequest(url,
                        formdata=data1,
                        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.3; en-US; rv:37.0) Gecko/20100101 Firefox/37.0',
                        'Referer':"http://epub.sipo.gov.cn"},
                        callback=self.getpages,dont_filter=True)


    def getpages(self,response):
        hxs = response.selector
        totalPage = hxs.xpath(u"//input[@id='pn']/@onkeypress").re("zl_tz\((\d{1,})\)")[0]
        url = "http://epub.sipo.gov.cn/patentoutline.action"
        # print totalPage, "i'm totalPage"
        data = self.rawData
        # strWord = "公开（公告）号='CN201310%' or 申请日,公开（公告）日,\
        # 进入国家日期+='2013.10' or 申请号,本国优先权,分案原申请号+='201310%'\
        #  or 申请（专利权）人,发明（设计）人,代理人,优先权,本国优先权,\
        #  分案原申请号,生物保藏,国际申请,国际公布+='%201310%' or \
        #  地址,名称,专利代理机构,摘要+='201310'"
        strWord = hxs.xpath("//script[contains(text(), \
                'function setup(ksjs)')]").re(r"strWord.value = \"([\W\S]*?)\";")[0]
        # print strWord, "i'm strWord extract from page"
        data1 = {"showType":"1",'strWord':"",
            "numSortMethod":"4","strLicenseCode":"",
            "selected":"","numFMGB":"0","numFMSQ":"","numSYXX":"",
            "numWGSQ":"","pageSize":"20","pageNow":"1"}
        # print bytes(strWord), "i'm bytes strWord"
        data1["strWord"] = bytes(strWord)  #从页上提取strWord
        # strWord1 = "公开（公告）号='CN198601%' or 申请日,公开（公告）日,\
        # 进入国家日期+='1986.01' or 申请（专利权）人,发明（设计）人,代理人,优先权,\
        # 本国优先权,分案原申请号,生物保藏,国际申请,国际公布+='%198601%' or \
        # 地址,名称,专利代理机构,摘要+='198601'"
        # data1["strWord"] = strWord1
        # print strWord1, "i'm strWord direct"
        for i in range(int(totalPage)+1)[1:]:   #请求页面数控制,是从1开始的不是0
            data1["pageNow"] = str(i)
            # print "i'm page1"
            wrongpage = data1['pageNow']
            wrongstrWord = data1['strWord']
            yield FormRequest(url,
                    formdata=data1,
                    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.3; en-US; rv:37.0) Gecko/20100101 Firefox/37.0'},
                    callback=lambda response, wrongstrWord=wrongstrWord,wrongpage=wrongpage:self.detail(response,wrongstrWord,wrongpage),dont_filter=True) 

    def detail(self,response,wrongstrWord,wrongpage):
        # item =PersonMore()
        # print "detail response"
        if response.status != 200:
            item = unDownItem()
            item['wrongpage'] = wrongpage
            item['wrongstrWord'] = wrongstrWord
            yield item

        else:
            item = PatentItem()
            hxs = response.selector
            rawXpath = hxs.xpath(u"//div[@class='cp_box']")
            for i in rawXpath:
                # print "rawXpath work"
                item = PatentItem()
                fName = i.xpath("//script[contains(text(), \
                    'function setup(ksjs)')]").re(r"CN([\d]{6})%")

                name = i.xpath(u".//h1/text()").extract()
                pat = ur"\]\W(.*)"
                if len(name) != 0:
                    name = re.findall(pat, name[0])
                else:
                    name.append("")
                # print name[0], "i'm name"
                pubId = i.xpath(".//li[1]/text()").re(r"CN.*")
                if len(pubId) != 0:
                    pass
                else:
                    pubId.append("")
                # print pubId[0], "i'm pubId"
                pubDate = i.xpath(u".//li[2]/text()").re(r"[\d]{4}\..*")
                if len(pubDate) != 0:
                    pass
                else:
                    pubDate.append("")                
                # print pubDate[0], "i'm pubDate"
                appId = i.xpath(u".//li[3]/text()").re(r"[\d].*")
                if len(appId) != 0:
                    pass
                else:
                    appId.append("")                
                # print appId[0], "i'm appId"
                appDate = i.xpath(u".//li[4]/text()").re(r"[\d]{4}\..*")
                if len(appDate) != 0:
                    pass
                else:
                    appDate.append("")
                # print appDate[0], "i'm appDate"
                appPerson = i.xpath(u".//li[5]/text()").re(ur"申请人：(\S*)")
                # print appPerson[0], "i'm appPerson"
                inventor = i.xpath(u".//li[contains(text(),'发明人')]/text()").re(ur"发明人：([\S\W]*)")
                if len(inventor) != 0:
                    pass
                else:
                    inventor.append("")
                # print inventor, "i'm inventor[0]"

                addr = i.xpath(u".//li[8]/text()").re(ur"地址：(\S*)")
                if len(addr) != 0:
                    pass
                else:
                    addr.append("")                
                # print addr[0], "i'm addr[0]"
                classId = i.xpath(u".//li[contains(text(),'分类号')]/text()").re(ur"([A-Z].*?)[\s]")
                if len(classId) != 0:
                    pass
                else:
                    classId.append("")                
                # print classId[0], "i'm classId"
                agentEn = i.xpath(u".//li[9]/div/ul/li[contains(text(),'专利代理机构')]/text()").re(ur"专利代理机构：([\S\W]*)")
                # print agentEn, "i'm agentEn"
                agentPe = i.xpath(u".//li[9]/div/ul/li[contains(text(),'代理人')]/text()").re(ur"代理人：([\S\W]*)")
                # print agentPe, "i'm agentPe"
                abstract = i.xpath(u".//div[@class='cp_jsh']").re(ur"span>\s*?([\S]{1,2}[\s\S]*?。)<")
                pat = "<[\s\S]*?>"    #替换abstract中有<>的内容 
                if len(abstract) != 0:
                    abstract[0] = re.sub(pat, "", abstract[0])
                    # print abstract, "i'm abstract"
                else:
                    abstract.append("")

                item['fName'] = fName[0]
                item['name'] = name[0]
                item['pubId'] = pubId[0]
                item['pubDate'] = pubDate[0]
                item['appId'] =  appId[0]
                item['appDate'] = appDate[0]
                item['appPerson'] = appPerson[0]
                item['inventor'] = inventor[0]
                item['addr'] = addr[0]
                item['classId'] = classId[0]
                # # item['agentEn'] = agentEn
                if len(agentEn) != 0:
                    item['agentEn'] = agentEn[0]
                else:
                    agentEn.append('')
                    item['agentEn'] = agentEn[0]
                # # item['agentPe'] = agentPe
                if len(agentPe) != 0:
                    item['agentPe'] =agentPe[0]
                else:
                    agentPe.append('')
                    item['agentPe'] = agentPe[0]
                item['abstract'] = abstract[0]
                # print name[0], "i'm name"
                yield item
