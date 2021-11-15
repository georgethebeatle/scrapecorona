# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from os.path import exists


class FilterInvalidPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get('date'):
            raise DropItem(f"Missing date in {item}")

        if not adapter.get('new_cases'):
            raise DropItem(f"Missing new_cases in {item}")

        return item


class CsvWriterPipeline:

    filepath = 'covid.csv'

    def __init__(self):
        self.header = 'date,new_cases,deaths,'
        for age_group in range(20):
            self.header += f'{self.age_group_string(age_group)},'
        self.header = self.header[:-1]

    def open_spider(self, spider):
        file_exists = exists(self.filepath)
        self.file = open(self.filepath, 'a')
        if not file_exists:
            self.file.write(self.header + '\n')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = ""

        for key in self.header.split(','):
            if key in item:
                line += f'{item[key]},'
            else:
                line += '0,'
        line = line[:-1]

        self.file.write(line + '\n')
        return item

    def age_group_string(self, age_group):
        return f'{age_group * 5}-{(age_group + 1) * 5 - 1}'
