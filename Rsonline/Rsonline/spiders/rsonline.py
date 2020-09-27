# -*- coding: utf-8 -*-
import scrapy
from Rsonline.items import RsonlineItem
class RsonlineSpider(scrapy.Spider):
    name = 'rsonline'
    allowed_domains = ['rsonline.cn']
    start_urls = ['https://rsonline.cn/web/']
    def parse(self,response):
        # first_urls = response.xpath("//ul[@class='column1']//li/a/@href").getall()

        yield scrapy.Request(self.start_urls[0], callback=self.parsee, meta={"middlemare": "rsonDownloaderMiddleware"})

    def parsee(self, response):
        first_urls = response.xpath("//ul[@class='column1']//li/a/@href").getall()
        # print(len(first_urls))  372
        for first_url in first_urls[15:16]:
            # print("-------")
            # print("https://rsonline.cn" + first_url)
            first_url = "https://rsonline.cn" + first_url
            # print(first_url)
            yield scrapy.Request(first_url,callback=self.second_process)
            # break

    def second_process(self,response):
        second_urls = response.xpath("//div[@class='cell']/div/a/@href").getall()
        for second_url in second_urls:
            yield scrapy.Request("https://rsonline.cn" + second_url,callback=self.third_process)
        # print("https://rsonline.cn" + second_url)  # https://rsonline.cn/web/c/pcb-prototyping/emi-rfi-shielding-materials/shielding-sheets/


    def third_process(self,response):
        # final_urls = response.xpath("//div[contains(@class,'margin-bottom')]/a/@href").getall()
        totals = response.xpath("//span[@class='number']/text()").get()
        # url = response.body_as_unicode()
        url = response.request.url
        # print(url,totals)
        totals = float(totals)
        if totals < 20.0:
            pages = 1
        else:
            totals = totals / 20
            list_total = str(totals).split('.')
            if float(list_total[1]) == 0:
                pages = totals
            else:
                pages = totals + 1
        # print(pages)
        # print(url)
        for i in range(int(pages)):
            # print(url + "?pn=" + str(i + 1))
            yield scrapy.Request(url + "?pn=" + str(i + 1), callback=self.get_other_page)

    def aa(self,url,totals):
        # print("aa 函数已调用")
        totals = float(totals)
        if totals < 20.0:
            pages = 1
        else:
            totals = totals / 20
            list_total = str(totals).split('.')
            if float(list_total[1]) == 0:
                pages = totals
            else:
                pages = totals + 1
        # print(pages)
        # print(url)
        for i in range(int(pages)):
            print(url + "?pn=" + str(i + 1))
            yield scrapy.Request(url + "?pn=" + str(i + 1),callback=self.get_other_page)

    def get_other_page(self,response):
        final_urls = response.xpath("//div[contains(@class,'margin-bottom')]/a/@href").getall()
        for url in final_urls:
            yield scrapy.Request("https://rsonline.cn" + url,callback=self.final_process)
    def final_process(self,response):
        # 获取商品价格
        try:
            item = RsonlineItem()
            #含税价
            vat_price =  response.xpath("//span[contains(@class,'price txt-vat')]/text()").get()
            RMB = response.xpath("//span[@class='priceCurrency']/text()").get()
            pric = response.xpath("//span[@class='price']/text()").get()
            price = RMB + " " + pric
            # "".join(list(filter(lambda ch: ch in '1234567890.', price)))
            #名称
            name = response.xpath("//h1[contains(@class,'main-page-header')]/text()").get().strip()
             # 品牌
            brand = response.xpath("//span[@class='keyValue']/a/span/text()").get()
             # 零件编号
            bianhao = response.xpath("//span[contains(@class,'bold')]/span/text()").get()
            # 单位
            danwei = response.xpath("//div[@class='txt']/text()").get()
            danwei2 = " "
             # 单位明细
            if '(' in danwei:
                list = danwei.split(' ')
                danwei2 = list[-1]
                list.pop()
                danwei ="".join(list)
            # print(name + '\n' + brand + '\n' + price + '\n' + bianhao + '\n' + danwei + '\n' + danwei2)
            item['per_unit1'] = ""
            item['per_unit2'] = ""
            item['per_unit3'] = ""
            item['per_unit4'] = ""
            item['per_unit5'] = ""
            item['per_unit6'] = ""
            item['per_unit7'] = ""
            item['per_unit8'] = ""
            item['per_unit9'] = ""
            item['per_unit10'] = ""
            item['per_unit11'] = ""
            item['per_unit12'] = ""
            item['per_unit13'] = ""
            item['per_unit14'] = ""
            item['per_unit15'] = ""

            m = 1

            list = response.xpath("//div[@class='price-table']/div[contains(@class,'table-row')]/div/text()").getall()
            if '*' in list[2]:
                for iii in range(len(list)):
                    list[iii] = list[iii].strip()
                length = int((len(list)))
                for im in range(3,length):
                    item["per_unit" + str(m)] = list[im]
                    m = m + 1
            else:
                for i in range(len(list)):
                    list[i] = list[i].strip()
                length = int((len(list)))
                for i in range(2,length):
                    if m == 3 or m == 6 or m == 9 or m ==12 or m == 15:
                        item["per_unit" + str(m)] = " "
                        item["per_unit" + str(m + 1)] = list[i]
                        m = m + 2
                    else:
                        item["per_unit" + str(m)] = list[i]
                        m = m + 1
                    # string = ""

            item['name'] = name
            item['price'] = price
            item['bianhao'] = bianhao
            item['danwei'] = danwei
            item['danwei2'] = danwei2
            item['brand'] = brand
            yield item
        except Exception as e:
            print(e)