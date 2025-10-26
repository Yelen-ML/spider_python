# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv


class NewsPipeline:
    def open_spider(self, spider):
        self.f=open('a.csv', 'w+',encoding='utf-8',newline='')
        self.writer=csv.DictWriter(self.f,fieldnames=['content','title','time'])
        self.writer.writeheader()
    def process_item(self, item, spider):
        self.writer.writerow(item)
    def close_spider(self, spider):
        self.f.close()
