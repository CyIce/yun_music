# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from yun_music.items import SingerItem, AlbumItem, SongItem
import json


class YunMusicPipeline(object):

    def __init__(self):
        self.fsong = open("song.out", "w")
        self.falbum = open("album.out", "w")

    def process_item(self, item, spider):

        if isinstance(item, SongItem):
            print(json.dumps(item))
            self.fsong.writelines(json.dumps(dict(item)) + ",\n")

        elif isinstance(item, AlbumItem):

            self.falbum.writelines(json.dumps(item) + ",")


        elif isinstance(item, SongItem):
            pass

        return item

    def close_spider(self, spider):
        self.fsong.close()
        self.falbum.close()
