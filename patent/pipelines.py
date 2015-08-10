# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os


class PatentPipeline(object):
    def process_item(self, item, spider):
        if len(item.values()) == 2:
            os.chdir("/root/dyh/data/testScrapyd")
            f = open("undownpage", "a")
            writeIn = item['wrongpage'] + "\001" + item['wrongstrWord']
            f.write(writeIn+"\n")
            f.close()
        else:
            os.chdir("/root/dyh/data/testScrapyd")
            result = tuple(item.values())
            f = open(item['fName'], "a")
            writeIn = "\001".join(result)
            f.write(writeIn+"\n")
            f.close()
        # for val in result_list:
        #     writeIn = "\001".join(val)
        #     f.write(writeIn+"\n")
        #     print writeIn
        # f.close()
