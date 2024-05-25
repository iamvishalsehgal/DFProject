# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import csv

class CrawlerPipeline:
    def open_spider(self, spider):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', spider.name, 'results.csv')
        self.existing_data = self.read_existing_data()
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = None

    def close_spider(self, spider):
        self.file.close()

    def read_existing_data(self):
        if not os.path.exists(self.file_path):
            return set()
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return {self.make_hashable(row) for row in reader}

    def process_item(self, item, spider):
        item_hashable = self.make_hashable(ItemAdapter(item).asdict())
        if item_hashable not in self.existing_data:
            if self.writer is None:
                self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
                if not self.file.tell():
                    self.writer.writeheader()
            self.writer.writerow(item)
            self.existing_data.add(item_hashable)
        return item

    def make_hashable(self, item):
        """Recursively make item hashable."""
        if isinstance(item, dict):
            return frozenset((key, self.make_hashable(value)) for key, value in item.items())
        if isinstance(item, list):
            return tuple(self.make_hashable(x) for x in item)
        return item
