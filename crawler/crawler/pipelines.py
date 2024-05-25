import os
import csv
from itemadapter import ItemAdapter
import logging

class CrawlerPipeline:
    def open_spider(self, spider):
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', spider.name, 'results.csv')
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)  # Ensure the directory exists
        self.processed_urls = set()
        self.fieldnames = ['url', 'wallet_addresses']
        
        # Read existing data
        self.existing_data = self.read_existing_data()
        
        # Open the file in append mode
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        
        # If the file is new, write the header
        if os.path.getsize(self.file_path) == 0:
            self.writer.writeheader()
        
        logging.info(f"Pipeline opened. Existing data: {self.existing_data}")

    def close_spider(self, spider):
        self.file.close()
        logging.info("Pipeline closed.")

    def read_existing_data(self):
        if not os.path.exists(self.file_path):
            logging.info("No existing data file found.")
            return set()
        with open(self.file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = {row['url'] for row in reader}
            logging.info(f"Read existing data: {data}")
            return data

    def process_item(self, item, spider):
        item_dict = ItemAdapter(item).asdict()
        item_url = item_dict.get('url')
        
        logging.info(f"Processing item: {item_dict}")

        if item_url and item_url not in self.existing_data:
            logging.info(f"New item found: {item_dict}")
            self.existing_data.add(item_url)
            self.writer.writerow(item_dict)
            spider.logger.info(f"Item written: {item_dict}")
        else:
            logging.info(f"Duplicate item found and skipped: {item_dict}")
            spider.logger.info(f"Duplicate item found and skipped: {item_dict}")

        return item

# Ensure that logging is properly configured
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
