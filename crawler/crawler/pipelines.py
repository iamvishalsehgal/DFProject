import csv
import os
from itemadapter import ItemAdapter

class CrawlerPipeline:
    def open_spider(self, spider):
        self.wallet_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'wallet_spider', 'wallets.csv')
        self.av_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'AVCrawler', 'sellers.csv')
        
        if spider.name == 'wallet_spider':
            self.file_path = self.wallet_file_path
            self.fieldnames = ['url', 'wallet_addresses']
        elif spider.name == 'AVCrawler':
            self.file_path = self.av_file_path
            self.fieldnames = None  # Will be determined dynamically
        
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.existing_data = self.read_existing_data()
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = None  # Will be initialized after determining fieldnames

    def close_spider(self, spider):
        self.file.close()

    def read_existing_data(self):
        if not os.path.exists(self.file_path):
            return {'data': set(), 'fieldnames': set()}
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames if reader.fieldnames else []
            data = {row['url'] for row in reader} if 'url' in fieldnames else set()
            return {'data': data, 'fieldnames': set(fieldnames)}

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        if spider.name == 'wallet_spider':
            url = item_dict.get('url')
            if url and url not in self.existing_data['data']:
                self.existing_data['data'].add(url)
                if self.writer is None:
                    self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
                    if os.path.getsize(self.file_path) == 0:
                        self.writer.writeheader()
                self.writer.writerow(item_dict)
                spider.logger.info(f"Item written: {item_dict}")
            else:
                spider.logger.info(f"Duplicate item found and skipped: {item_dict}")
        elif spider.name == 'AVCrawler':
            item_dict.pop('url', None)  # Remove the 'url' field for AVCrawler items
            if self.writer is None:
                self.initialize_writer(item_dict)
            else:
                # Check if new fields are found and update the CSV file accordingly
                new_fields = set(item_dict.keys()) - set(self.fieldnames)
                if new_fields:
                    self.fieldnames = list(self.fieldnames) + list(new_fields)
                    self.update_csv_file()

            self.writer.writerow(item_dict)
            spider.logger.info(f"Item written: {item_dict}")
        return item

    def initialize_writer(self, item_dict):
        # Initialize the writer with dynamic fieldnames
        if self.fieldnames is None:
            self.fieldnames = list(item_dict.keys())
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        if os.path.getsize(self.file_path) == 0:
            self.writer.writeheader()
        else:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                existing_headers = f.readline().strip()
            if not existing_headers:
                self.writer.writeheader()

    def update_csv_file(self):
        # Read existing data
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        # Write the updated CSV file with new headers
        with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        # Reopen the file for appending
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)

    def make_hashable(self, item):
        """Recursively make item hashable."""
        if isinstance(item, dict):
            return frozenset((key, self.make_hashable(value)) for key, value in item.items())
        if isinstance(item, list):
            return tuple(self.make_hashable(x) for x in item)
        return item
