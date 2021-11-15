import scrapy
import dateparser


class CovidSpider(scrapy.Spider):
    name = "covid"
    start_urls = [
        'https://coronavirus.bg/bg/',
    ]

    def __init__(self):
        with open('lowerbound.txt', 'r') as f:
            self.lower_bound = int(f.read())
        super().__init__(self.name)

    def parse(self, response):
        self.log(f'Scraping index page {response.url}')

        latest_news = response.css('.news-more::attr(href)')
        if len(latest_news) > 0:
            upper_bound = int(latest_news[0].re_first('/bg/news/([0-9]+)'))
            self.log(f'Crawling /bg/news/{self.lower_bound}..{upper_bound}')
            if upper_bound <= self.lower_bound:
                self.log('Nothing to do...')
                return
            for id in range(self.lower_bound, upper_bound):
                yield response.follow(f'/bg/news/{id}', callback=self.parse_newspage)
            with open('lowerbound.txt', 'w') as f:
                f.write(str(upper_bound))

    def parse_newspage(self, response):
        self.log(f'Scraping news page {response.url}')

        item = {}
        date = response.css('.single-news-date::text').get()
        if date:
            item['date'] = dateparser.parse(date).strftime("%d-%m-%Y")

        new_cases = response.css('.page-content-header::text').re_first('^([ 0-9]+[ 0-9]+).*денонощие')
        if new_cases:
            item['new_cases'] = new_cases.replace(' ', '')
            self.log(f'recording new cases: {item["new_cases"]}')

        deaths = response.css('::text').re('на ([0-9]+) г.')
        item['deaths'] = str(len(deaths))

        if len(deaths) > 0:
            deaths_by_age_group = self.deaths_by_age_group(deaths)
            for age_group, deaths in deaths_by_age_group.items():
                item[self.age_group_string(age_group)] = deaths
        yield item

    def deaths_by_age_group(self, deaths):
        deaths_by_age_group = {}

        for ageStr in deaths:
            age = int(ageStr)
            if age < 0 or age > 100:
                continue
            age_group = int(age / 5)
            if age_group in deaths_by_age_group:
                deaths_by_age_group[age_group] += 1
            else:
                deaths_by_age_group[age_group] = 1

        return deaths_by_age_group

    def age_group_string(self, age_group):
        return f'{age_group * 5}-{(age_group + 1) * 5 - 1}'
