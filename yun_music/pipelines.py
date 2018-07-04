# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

from yun_music.items import SingerItem, AlbumItem, SongItem


class YunMusicPipeline(object):

    def __init__(self):
        self.fsong = open("song.json", "wb")
        self.falbum = open("album.json", "wb")
        self.fsinger=open("singer.json","wb")
        self.fsong.write("[".encode("utf-8"))
        self.falbum.write("[".encode("utf-8"))
        self.fsinger.write("[".encode("utf-8"))


    def process_item(self, item, spider):

        if isinstance(item, SongItem):
            jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.fsong.write(jsontext.encode("utf-8"))

        elif isinstance(item, AlbumItem):
            jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.falbum.write(jsontext.encode("utf-8"))

        elif isinstance(item, SingerItem):
            jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
            self.fsinger.write(jsontext.encode("utf-8"))


        return item

    def close_spider(self, spider):
        self.fsong.write("{}".encode("utf-8"))
        self.fsong.write("]".encode("utf-8"))

        self.fsinger.write("{}".encode("utf-8"))
        self.fsinger.write("]".encode("utf-8"))

        self.falbum.write("{}".encode("utf-8"))
        self.falbum.write("]".encode("utf-8"))

        self.fsong.close()
        self.falbum.close()
        self.fsinger.close()
