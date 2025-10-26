import scrapy
from urllib.parse import urljoin
from news.items import NewsItem

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.szpu.edu.cn"]
    start_urls = ["https://www.szpu.edu.cn/xwzt/szyw.htm"]

    def parse(self, response):
        lis=response.css("ul.list23 > li")
        for li in lis:
            a=urljoin("https://www.szpu.edu.cn",li.css("a::attr(href)").get())
            b=li.css("div.txt > h4::text").get()
            c=li.css("div.txt > h6::text").get()
            yield scrapy.Request(a,callback=self.parse_data,meta={"c":c,"b":b})    
            
    def parse_data(self, response):
        ps=response.css("div.v_news_content > p")
        ls=[]
        for p in ps:
            content=p.css("::text").get(default="")
            ls.append(content)
        contents="\n".join(ls)
        item=NewsItem()
        item["time"]=response.meta["c"]
        item["title"]=response.meta["b"]
        item["content"]=contents
        yield item

    
