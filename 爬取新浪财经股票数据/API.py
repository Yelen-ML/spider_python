import requests
def get_data(url):
    # 发送GET请求，获取响应
    res = requests.get(url)
    # 遍历响应的JSON数据
    for i in res.json():
        yield (i["code"], i["open"], i["high"], i["low"])
urls = ["https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page={}&num=40&sort=symbol&node=sh_a&s_r_a=page".format(1)]
f = open("sina_stock_data.txt", "a+")

for url in urls:
    for data in get_data(url):
        f.writelines(",".join(data))
        f.write("\n")
f.close()