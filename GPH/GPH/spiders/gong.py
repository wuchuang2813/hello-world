# -*- coding: utf-8 -*-
import scrapy
from GPH.items import GphItem

class GongSpider(scrapy.Spider):
    name = 'gong'
    allowed_domains = ['vipmro.com']
    start_urls = ['http://vipmro.com/']

    def parse(self, response):
        yield scrapy.Request(self.start_urls[0],callback=self.parsse,meta={"middlemare":"gphDownloaderMiddleware"})

    def parsse(self,response):

        # list = response.xpath(
        #     "//div[@class='category-body']//div[@class='subcategory-item']//div[@class='item-list']//a/@href").getall()
        list = response.xpath(
            "//div[@class='m-categories-list']/div[contains(@class,'categories-item')]//div[@class='category-body']//div[@class='subcategory-list']//div[@class='item-list']//a/@href").getall()
        # print('------------------')
        # print(len(list))    #总数 ： 1039
        for link in list[200:500]:
            link = 'http://vipmro.com/' + link
            # print(link)
            yield scrapy.Request(link, callback=self.parse_list)
            # break
    def get_pages(self,response):
        pages = response.xpath("//div[@class='m-pagination']//a/@href").getall()
        for page in pages:
            page = "http://vipmro.com/" + page
            yield scrapy.Request(page, callback=self.parse_other_pages)
    def parse_other_pages(self,response):
        detail_urls = response.xpath("//div[@class='goods-info']/a/@href")
        for detail_url in detail_urls:
            # print(detail.get())
            detail_url = 'http://vipmro.com/' + detail_url.get()
            # print(detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_detail)
            # print(page)
    def parse_list(self,response):
        self.get_pages(response)
        detail_urls = response.xpath("//div[@class='goods-info']/a/@href")
        for detail_url in detail_urls:
            # print(detail.get())
            detail_url = 'http://vipmro.com/' + detail_url.get()
            # print(detail_url)
            yield scrapy.Request(detail_url,callback=self.parse_detail)
            # break
    def parse_detail(self,response):
        try :
            name = response.xpath("//div[@class='m-product-info']/h1[@class='product-title']/text()").get().strip().split(",")[0]
            huohao = response.xpath("//table[@class='product-pros m-top20']//tr/td/text()").get()
            bianhao = response.xpath("//div[@class='pics-bottom']/text()").get().strip().split("：")[1]
            huoqi = response.xpath("//tr[@class='J_delivery']/td/text()").get()
            pric = response.xpath("//span[@class='J_loginPrice']/text()").get()
            unit = response.xpath("//span[@class='price-current']/text()").getall()[1].strip()
            # price = pric + unit
            xinghao = response.xpath("//table[contains(@class,'m-top20')]/tr[2]/td/text()").get()
            weight = response.xpath("//table[contains(@class,'m-top20')]/tr[3]/td/text()").get()
            if ('kg' in weight):
                weight = weight
            else:
                weight = "无"
            if ('/' in weight):
                bzsl = weight
            else:
                bzsl = response.xpath("//table[contains(@class,'m-top20')]/tr[4]/td/text()").get().strip()
            # print("----------------------")
            # print(name)
            yield GphItem(name=name, huoqi=huoqi, huohao=huohao, bianhao=bianhao, pric=pric,unit=unit,xinghao=xinghao,
                                  weight=weight, bzsl=bzsl)
        except:
            print("无")

