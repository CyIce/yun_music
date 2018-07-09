import json
import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver

from yun_music.items import SingerItem, AlbumItem, SongItem


class yun_music_spider(scrapy.Spider):
    # 爬虫名称
    name = "music_spider"
    # 爬虫的允许域范围
    allowed_domains = ['music.163.com']
    # 爬虫起始url
    start_urls = ['https://music.163.com/#/discover/artist/cat?id=1001']
    # 基础url，用于拼接url
    base_url = "https://music.163.com/#"
    # 爬虫已爬取的次数
    crawl_times = 0
    crawl_album_times = 0
    crawl_song_times = 0
    crawl_lyric_times = 0
    times = 0

    def __init__(self):
        #
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):

        yield scrapy.Request(url=response.url, callback=self.parse_singer_list, dont_filter=True)

        # yield scrapy.Request(url=response.url, callback=self.parse_singer_list, dont_filter=True)

        # singer_type = [1003, 1002]
        # , 2001, 2002, 2003, 4001, 4002, 4003, 6001, 6002, 6003, 7001, 7002, 7003]
        # singer_cha = [80, 81, 82, 83, 84, 85, 86]
        # [0, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,89, 90]

        # singer_type = [1001]
        # singer_cha = [65]

        #for i in singer_type:
            # singer_list_url = "https://music.163.com/#/discover/artist/cat?id=%d&initial=%d" % (i, j)
            #singer_list_url = "https://music.163.com/#/discover/artist/cat?id=%d" % i
           # print (singer_list_url)
            # yield scrapy.Request(url=singer_list_url, callback=self.parse_singer_list, dont_filter=True)

    def parse_singer_list(self, response):
        # 歌手主页列表
        singer_homes = response.xpath("//a[starts-with(@href,'/artist?id=')]")
        for singer_home in singer_homes:
            short_url = singer_home.xpath("./@href").extract()[0]
            short_url_album = short_url.replace("artist", "artist/album")
            short_url_singer = short_url.replace("artist", "artist/desc")
            # 歌手专辑页面的URL
            singer_album_url = self.base_url + short_url_album
            singer_brief = self.base_url + short_url_singer
            self.crawl_times+=1

            yield scrapy.Request(url=singer_album_url, callback=self.parse_album, dont_filter=True)
            yield scrapy.Request(url=singer_brief, callback=self.parse_singer, dont_filter=True)

    # 爬取歌手信息
    def parse_singer(self, response):
        singer_item = SingerItem()
        node = response.xpath("/html/body/div/div/div/div/div")
        # 歌手名字
        singer_name = node.xpath("./div/h2/text()").extract()[0]
        # 歌手头像
        singer_photo = node.xpath("./img/@src").extract()[0]
        # 歌曲简介
        singer_introduction = node.xpath("./div/p/text()").extract()[0]
        # 专辑数量
        song_count=node.xpath("./div/p[@class='z-indent']")[0].xpath("./br")
        print (song_count)

        b

        singer_item['singer_name'] = singer_name
        singer_item['singer_photo'] = singer_photo
        singer_item['singer_introduction'] = singer_introduction

        print(singer_name)

        yield singer_item

    # 爬取歌手的专辑的url
    def parse_album(self, response):

        album_list = response.xpath("/html/body/div/div/div/div/ul[@id='m-song-module']/li")

        for album in album_list:

            short_url = album.xpath("./div/a/@href").extract()[0]
            album_url = self.base_url + short_url
            self.crawl_album_times += 1
            yield scrapy.Request(url=album_url, callback=self.parse_song, dont_filter=True)

        next_page = response.xpath("//div/div/a[@class='zbtn znxt']/@href")
        if next_page != []:
            next_page = next_page.extract()[0]
            next_page = self.base_url + next_page
            yield scrapy.Request(url=next_page, callback=self.parse_album, dont_filter=True)

    # 解析歌曲信息
    def parse_song(self, response):

        album_item = AlbumItem()

        album_info = response.xpath("//div[@class='cnt']/div[@class='cntc']/div[@class='topblk']")

        album_name = album_info.xpath("./div/div/h2/text()").extract()[0]

        singer = album_info.xpath("./p/span/@title").extract()[0]

        punish_time = album_info.xpath("./p/text()").extract()[0]

        album_photo = response.xpath("//div/div[@class='cover u-cover u-cover-alb']/img/@src").extract()[0]

        album_introduction = response.xpath("//div[@class='n-albdesc']/p/text()")

        if album_introduction != []:
            album_introduction = album_introduction.extract()[0]
        else:
            album_introduction = "无"

        song_list = response.xpath("/html//div[@id='song-list-pre-cache']//tbody/tr")

        album_item['album_name'] = album_name
        album_item['album_photo'] = album_photo
        album_item['album_introduction'] = album_introduction
        album_item['album_singer'] = singer

        yield album_item

        for song_info in song_list:
            song_id = song_info.xpath("./td[2]/div/div/div/span/a/@href").extract()[0]
            song_id = song_id.replace("/song?id=", "")
            song_name = song_info.xpath("./td[2]/div/div/div/span/a/b/@title").extract()[0]
            lyric_url = "https:/music.163.com/#/api/song/lyric?id={}&lv=1&kv=1&tv=1".format(song_id)

            ret = {'song_id': song_id, "song_name": song_name, "song_singer": singer, "punish_time": punish_time,
                   "song_album": album_name, "song_photo": album_photo}

            yield scrapy.Request(url=lyric_url, meta=ret, callback=self.parse_lyric,
                                 dont_filter=True)

    # 解析歌词
    def parse_lyric(self, response):
        song_item = SongItem()

        lyric = response.xpath("/html/body/text()").extract()[0]
        lyric = lyric.replace("\\n", "")
        song_item['song_id'] = response.meta["song_id"]
        song_item['song_name'] = response.meta["song_name"]
        song_item['song_singer'] = response.meta["song_singer"]
        song_item['punish_time'] = response.meta["punish_time"]
        song_item['song_album'] = response.meta["song_album"]
        song_item['song_photo'] = response.meta["song_photo"]

        song_item["song_lyric"] = lyric
        yield song_item

    def spider_closed(self, spider):
        self.browser.quit()
