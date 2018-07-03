import scrapy
from yun_music.items import SingerItem, SongItem
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from pyvirtualdisplay import Display


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

        singer_type = [1001]
        singer_cha = [65]

        for i in singer_type:
            for j in singer_cha:
                singer_list_url = "https://music.163.com/#/discover/artist/cat?id=%d&initial=%d" % (i, j)
                yield scrapy.Request(url=singer_list_url, callback=self.parse_singer_list, dont_filter=True)

        # yield scrapy.Request("https://music.163.com/#/discover/artist/cat?id=1001&initial=66", callback=self.parse)

    def parse_singer_list(self, response):

        # 歌手主页列表
        singer_homes = response.xpath("//a[starts-with(@href,'/artist?id=')]")

        for singer_home in singer_homes:
            short_url = singer_home.xpath("./@href").extract()[0]
            short_url = short_url.replace("artist", "artist/album")
            # 歌手专辑页面的URL
            singer_album_url = self.base_url + short_url
            self.crawl_times += 1
            if self.crawl_times <= 1:
                yield scrapy.Request(url=singer_album_url, callback=self.parse_album, dont_filter=True)

    # 爬取歌手的专辑的url
    def parse_album(self, response):

        album_list = response.xpath("//html/body/div/div/div/div/ul[@class='m-cvrlst m-cvrlst-alb4 f-cb']/li")
        for album in album_list:
            short_url = album.xpath("//div/a[@href").extract()
            print(short_url)
            album_url = self.base_url + short_url
            print(album_url)
            yield scrapy.Request(url=album_url, callback=self.parse_song, dont_filter=True)

    def parse_song(self, response):
        pass

    def spider_closed(self, spider):
        self.browser.quit()
