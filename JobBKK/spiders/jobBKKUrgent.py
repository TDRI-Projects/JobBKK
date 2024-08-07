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
class jobBKKSpider2(CrawlSpider):
    name = "jobBKKUrgent"
    allowed_domains = ["www.jobbkk.com"]
    start_urls = ["https://www.jobbkk.com/jobs/urgent"]
    rules = [
        #Rule(LinkExtractor(allow=r'\?page=\d+'), callback="check_date", follow=True),
        Rule(LinkExtractor(restrict_xpaths ='//*[contains(@class,"pagination")]'), callback = "check_date",follow=True),
        Rule(LinkExtractor(restrict_xpaths ='//*[contains(@class,"step2")]'), callback="parse", follow=True)
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div/div[5]/div/div'), callback="check_date", follow=True)
    ]

    def check_date(self, response):
        last_posting = response.xpath('string(//*[contains(@class,"time-company")])')[-1].extract().strip()
        if last_posting == '1 วันก่อน':
            raise CloseSpider
        pass
        
    def parse(self, response):
        job_location = response.xpath('string(//p[span[contains(text(), "สถานที่ปฏิบัติงาน :")]])').get()
        job_group = response.xpath('string(//p[span[contains(text(), "สาขาอาชีพหลัก :")]])').get()
        contract_type = response.xpath('string(//p[span[contains(text(), "รูปแบบงาน :")]])').get()
        positions = response.xpath('string(//p[span[contains(text(), "จำนวนที่รับ :")]])').get()
        salary = response.xpath("string(//p[span[contains(text(), 'เงินเดือน(บาท) :')]])").get()
        gender = response.xpath("string(//p[span[contains(text(), 'เพศ :')]])").get()
        age = response.xpath("string(//p[span[contains(text(), 'อายุ(ปี) :')]])").get()
        education = response.xpath("string(//p[span[contains(text(), 'ระดับการศึกษา :')]])").get()
        responsibilities = response.xpath('string(//section[./p[contains(text(), "หน้าที่ความรับผิดชอบ")]])').get()
        qualifications = response.xpath('string(//section[./p[contains(text(), "คุณสมบัติด้านความรู้และความสามารถ")]])').get()
        
        yield{
            'job_location':job_location,
            'job_group':job_group,
            'contract_type': contract_type,
            'positions': positions,
            'salary':salary,
            'gender':gender,
            'age':age,
            'education':education,
            'details': responsibilities + qualifications
            
        }