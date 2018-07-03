# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SingerItem(scrapy.Item):

    # 歌手信息
    # 歌手名
    singer_name=scrapy.Field()
    # 歌手照片
    singer_photo = scrapy.Field()
    # 歌手的单曲数目
    song_count = scrapy.Field()
    # 歌手的专辑数目
    album_count = scrapy.Field()
    # 歌手的mv数目
    mv_count = scrapy.Field()
    # 歌手的简介
    singer_introduction = scrapy.Field()
    # 歌手的热度
    singer_fire = scrapy.Field()
    # 歌手界面的url
    singer_url=scrapy.Field()

class SongItem(scrapy.Item):
    # 歌曲的信息
    # 歌曲的名称
    song_name=scrapy.Field()
    # 歌曲的演唱者
    singer = scrapy.Field()
    # 歌曲发布时间
    punish_time = scrapy.Field()
    # 歌曲的热度
    song_fire = scrapy.Field()
    # 歌曲封面
    song_photo = scrapy.Field()
    # 歌曲的id
    song_id= scrapy.Field()
    # 歌曲的专辑
    song_album=scrapy.Field()





