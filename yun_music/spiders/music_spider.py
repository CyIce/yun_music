import scrapy
from yun_music.items import SingerItem, SongItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

import time

class yun_music_spider(scrapy.Spider):
    # 爬虫名称
    name = "music_spider"
    # 爬虫的允许域范围
    allowed_domains = ['music.163.com']
    # 爬虫起始url
    start_urls = ['https://music.163.com/#/discover/artist/cat?id=1001&initial=65']
    # 基础url，用于拼接url
    base_url = "https://music.163.com/#"
    # 爬虫已爬取的次数
    crawl_times = 0

    def __init__(self):
        self.browser = webdriver.Chrome()  # 指定使用的浏览器
        dispatcher.connect(self.spider_closed, signals.spider_closed)


    def parse(self, response):

        print(response.url)

        # 歌手列表
        singer_lists = response.xpath("//li/a[starts-with(@href,'/discover')]")
        # 歌手主页列表
        singer_homes = response.xpath("//a[starts-with(@href,'/artist?id=')]")

        for singer_list in singer_lists:
            short_url = singer_list.xpath("./@href").extract()[0]
            singer_list_url = self.base_url + short_url
            yield scrapy.Request(url=singer_list_url, callback=self.parse)

        for singer_home in singer_homes:
            short_url = singer_home.xpath("./@href").extract()[0]
            singer_home_url = self.base_url + short_url


        #yield scrapy.Request("https://music.163.com/#/discover/artist/cat?id=1001&initial=66", callback=self.parse)

    def parse_singer(self, response):
        pass

    def parse_song(self, response):
        pass

    def spider_closed(self, spider):
        self.browser.quit()
