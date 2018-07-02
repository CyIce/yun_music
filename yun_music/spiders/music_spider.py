import scrapy
from yun_music.items import SingerItem, SongItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


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

        # singer_type = [1001, 1002, 1003, 2001, 2002, 2003, 4001, 4002, 4003, 6001, 6002, 6003, 7001, 7002, 7003]
        # singer_cha = [0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,89, 90]

        singer_type=[1001]
        singer_cha=[65]

        for i in singer_type:
            for j in singer_cha:
                singer_list_url = "https://music.163.com/#/discover/artist/cat?id=%d&initial=%d" % (i, j)
                # print(singer_list_url)
                yield scrapy.Request(url=singer_list_url, callback=self.parse_singer_list, dont_filter=True)

        # yield scrapy.Request("https://music.163.com/#/discover/artist/cat?id=1001&initial=66", callback=self.parse)

    def parse_singer_list(self, response):

        # 歌手主页列表
        singer_homes = response.xpath("//a[starts-with(@href,'/artist?id=')]")

        f = open("log.txt", "w")

        for singer_home in singer_homes:
            short_url = singer_home.xpath("./@href").extract()[0]
            singer_home_url = self.base_url + short_url
            f.write(singer_home_url)
            yield scrapy.Request(url=singer_home_url, callback=self.parse_singer, dont_filter=True)
        f.close()

    def parse_singer(self, response):
        pass

    def parse_song(self, response):
        pass

    def spider_closed(self, spider):
        self.browser.quit()
