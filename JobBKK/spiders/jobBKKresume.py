import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
import re
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext
def remove_spaces(text):
# Use regex to replace multiple spaces with a single space
    return re.sub(r'\s+', ' ', text).strip()
class jobBKKSpiderResume(CrawlSpider):
    name = "jobBKKResume"
    allowed_domains = ["www.jobbkk.com"]
    start_urls = [#"https://www.jobbkk.com/resumes/lists/?&search_type=1&occupation=60",
                  "https://www.jobbkk.com/resumes/lists/?&search_type=1&occupation=" + str(x) for x in range(1,51)]
    rules = [
        #Rule(LinkExtractor(allow=r'\?page=\d+'), callback="check_date", follow=True),
        Rule(LinkExtractor(restrict_xpaths ='//*[@class="pagination"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths ='//*[@class="hover-detail-user clickShowDetail "]'), callback="parse", follow=True)
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div/div[5]/div/div'), callback="check_date", follow=True)
    ]

    def check_date(self, response):
        last_posting = response.xpath('string(//div[contains(@class, "time-company")])')[-1].extract().strip()
        # a_day_ago_thai = convert_date_to_thai_format(a_day_ago)
        # current_date_thai = convert_date_to_thai_format(current_date)    
        # if last_posting not in [current_date_thai, a_day_ago_thai]:
        #     raise CloseSpider
        pass
        
    def parse(self, response):
        last_posting = response.xpath('string(//div[contains(@class, "time-company")])')[-1].extract().strip()
        if last_posting == '1 วันก่อน':
            raise CloseSpider
        #resumes =  response.xpath('string(//div[contains(@class, "applying-detail")])').getall()
        resumes = response.xpath('//div[contains(@class, "applying-detail")]').getall()
        expected = response.xpath('//*[@class="expected"]').get()
        education = response.xpath('//*[@class="education"]').get()
        salary = response.xpath('//*[@class="salary"]/p//text()').get().strip()
        education = cleanhtml(education)
        education = education.splitlines()
        expected = cleanhtml(expected)
        expected = expected.splitlines()
        expected_list = [remove_spaces(line) for line in expected if line.strip()]
        education_list = [remove_spaces(line) for line in education if line.strip()]
        yield{
            'salary': salary,
            'expected': expected_list,
            'education': education_list
            
        }
        # print(cleanhtml(education))
        # print(type(resumes))
        # print(len(resumes))
        # for resume in resumes:
        #     job = cleanhtml(resume)
        #     job = job.splitlines()
        #     for line in job:
        #         print(line.strip())
    def close(self, reason):
        start_time = self.crawler.stats.get_value('start_time')
        finish_time = self.crawler.stats.get_value('finish_time')
        print("Total run time: ", finish_time-start_time)