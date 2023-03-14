# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
import sqlite3


class SQLitePipeLine:

    def open_spider(self, spider):
        db = os.getcwd()+'\\transcripts.db'
        # print('<----------------------->')
        # print(db)
        self.connection = sqlite3.connect(db)
        self.c = self.connection.cursor()

        # query
        self.c.execute(
            """CREATE TABLE IF NOT EXISTS transcripts(
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT)"""
        )
        self.connection.commit()

    def close_spider(slef, spider):
        slef.connection.close()

    def process_item(self, item, spider):
        self.c.execute("""
            INSERT INTO transcripts (title, plot, transcript, url) VALUES(?,?,?,?)
        """, (
            item['title'],
            item['plot'],
            item['transcript'],
            item['url'],
        ))
        self.connection.commit()
        return item
