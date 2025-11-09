#首次运行时使用，设置浏览器路径。后续运行时不需要再设置。
# from DrissionPage import ChromiumOptions
# path=r'C:\Program Files\Google\Chrome\Application\chrome.exe'
# ChromiumOptions().set_browser_path(path).save()
from DrissionPage import ChromiumPage
from pprint import pprint
import re
import csv
f=open('jd_data.csv','w',encoding='utf-8',newline='')
csv_writer=csv.DictWriter(f,fieldnames=['标题','原价','颜色','销量','卖点','店铺'])
csv_writer.writeheader()
dp=ChromiumPage()
dp.listen.start('api.m.jd.com/api?appid=search-pc-java&t')
dp.get('https://search.jd.com/Search?keyword=%E7%9B%B8%E6%9C%BA&enc=utf-8&wq=ccd&pvid=d6f6f51dd42a485da32485946c18e591')
next_page=dp.ele('text=下一页')
dp.scroll.to_see(next_page)
resp_list=dp.listen.wait(5)
for resp in resp_list:
    json_data=resp.response.body
    keys=json_data.keys()
    if 'abBuriedTagMap' in keys:
        for item in json_data['data']['wareList']:
            title = item['wareName'].replace('\n','')
            new_title=re.sub(r'<.*?>','',title)
            dit = {
                '标题': new_title,
                '原价': item['realPrice'],
                '颜色': item['color'],
                '销量': item['totalSales'],
                '卖点': item['sellingPoint'],
                '店铺':item['shopName'],
            }
            csv_writer.writerow(dit)