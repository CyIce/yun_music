import scrapy
from bs4 import BeautifulSoup

from yun_music.items import SingerItem,SongItem

class yun_music_spider(scrapy.Spider):

    # 爬虫名称
    name="music_spider"
    # 爬虫的允许域范围
    allowed_domains=['music.163.com']
    # 爬虫起始url
    start_urls=['https://music.163.com/#/discover/artist/cat?id=1001&initial=65']
    # 基础url，用于拼接url
    base_url="https://music.163.com/"
    # 爬虫已爬去的次数
    crawl_times=0


    def parse(self,response):

        soup=BeautifulSoup(response.body,'html.parser',from_encoding='utf-8')

        print("==================================================")
        print(soup)
        print("==================================================")


        #yield scrapy.Request("https://music.163.com/#/discover/artist/cat?id=1001&initial=66", callback=self.parse)


    def parse_singer(self,response):

        pass

    def parse_song(self,response):

        pass