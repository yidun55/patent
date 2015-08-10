# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PatentItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fName = Field()   #数据写入的文件名
    name = Field()   #发明公布
    pubId = Field()   #申请公布号
    pubDate = Field()    #申请公布日
    appId = Field()   #申请号
    appDate = Field()    #申请日
    appPerson = Field()   #申请人
    inventor = Field()   #发明人
    addr = Field()   #地址
    classId = Field()   #分类号
    agentEn = Field()   #专利代理机构
    agentPe = Field()     #代理人
    abstract = Field()   #摘要

class unDownItem(Item):
    wrongpage = Field()
    wrongstrWord = Field()