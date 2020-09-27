# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class GphPipeline:
    def __init__(self):
        self.wb = Workbook()  # 类实例化
        self.ws = self.wb.active  # 激活工作表
        # self.ws.append(['名称', '订货号', '货期', '价格', '商品编号', '商品型号', '重量', '包装数量'])  # 添加表头
        self.ws.append(['名称', '订货号', '货期', '价格','单位', '商品编号', '商品型号', '重量', '包装数量'])  # 添加表头


    def process_item(self, item, spider):
        data = [item["name"], item["huohao"], item["huoqi"], item["pric"],item["unit"],item["bianhao"], item["xinghao"],
                item['weight'], item['bzsl']]
        self.ws.append(data)  # 将数据以行的形式添加到工作表中
        self.wb.save('Earth.xlsx')  # 保存
        return item


# 另一种存储方式
from scrapy.exporters import CsvItemExporter

class EnrolldataPipeline(object):
    def open_spider(self, spider):
        self.file = open("/home/bladestone/enrolldata.csv", "wb")
        self.exporter = CsvItemExporter(self.file,
        fields_to_export=["schoolName", "currentBatch", "totalNumberInPlan"])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

import pymysql
#连接数据库
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        # port = '3306',
        user = "root",
        passwd = "root",
        charset = "utf8",
        use_unicode = False
    )
    return conn

class HellospiderPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE gph")
        #插入数据库
        sql = "INSERT INTO 数据(名称,订货号,货期,价格,单位,商品编号,商品型号,重量,包装数量) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            # name = name, huoqi = huoqi, huohao = huohao, bianhao = bianhao, pric = pric, unit = unit, xinghao = xinghao,
            # weight = weight, bzsl = bzsl
            cursor.execute(sql,
                           ( item['name'], item['huohao'], item['huoqi'], item['pric'], item['unit'], item['bianhao'], item['xinghao'], item['weight'], item['bzsl']))
            cursor.connection.commit()
        except BaseException as e:
            print("错误在这里>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<错误在这里")
            dbObject.rollback()
        return item
