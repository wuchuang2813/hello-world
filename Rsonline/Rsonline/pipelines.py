# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
class RsonlinePipeline:
    def __init__(self):
        self.wb = Workbook()  # 类实例化
        self.ws = self.wb.active  # 激活工作表
        # self.ws.append(['名称', '订货号', '货期', '价格', '商品编号', '商品型号', '重量', '包装数量'])  # 添加表头
        self.ws.append(['名称/描述', '价格', '编号', '单位','单位明细', '品牌','per_unit1','per_unit2','per_unit3','per_unit4','per_unit5','per_unit6','per_unit7','per_unit8','per_unit9','per_unit10','per_unit11','per_unit12','per_unit13','per_unit14','per_unit15'])  # 添加表头

    def process_item(self, item, spider):
        data = [item["name"], item["price"], item["bianhao"], item["danwei"], item["danwei2"], item["brand"],item["per_unit1"],item["per_unit2"],item["per_unit3"],item["per_unit4"],item["per_unit5"],item["per_unit6"],item["per_unit7"],item["per_unit8"],item["per_unit9"],item["per_unit10"],item["per_unit11"],item["per_unit12"],item["per_unit13"],item["per_unit14"],item["per_unit15"]]
        self.ws.append(data)  # 将数据以行的形式添加到工作表中
        self.wb.save('Earth.xlsx')  # 保存
        return item