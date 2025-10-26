import requests
import json
def get_data(url):
    response = requests.get(url)
    for i in response.json()['Data']['Posts']:
        yield i['RecruitPostName'], i['CountryName'], i['LocationName']
urls=['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1760278307296&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(i) for i in range(11)]
f=open("a.txt","a+",encoding="utf-8")
for url in urls:
    for i in get_data(url):
        f.writelines(",".join(i))
        f.write("\n")
f.close()