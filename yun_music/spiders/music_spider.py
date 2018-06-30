import scrapy

from yun_music.items import SingerItem,SongItem

class yun_music_spider(scrapy.Spider):

    # 爬虫名称
    name="music_spider"
    # 爬虫的允许域范围
    allowed_domains=[]
    # 爬虫其实url
    start_urls=[]
    # 基础url，用于拼接url
    base_url=""
    # 爬虫已爬去的次数
    crawl_times=0
<<<<<<< HEAD
    #
=======

>>>>>>> origin/master

    def parse(self,response):

        pass

    def parse_singer(self,response):

        pass

    def parse_song(self,response):

        pass