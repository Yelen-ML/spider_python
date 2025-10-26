import requests
from bs4 import BeautifulSoup
import json
h={"User-Agent":"Mozilla/5.0 (X11;Linux x86_64;rv:127.0) Gecko/20100101 Firefox/127.0" , "Cookie":"SUB=_2AkMfqlOIf8NxqwFRmvwTymvmZIxyzg3EieKp9qJTJRMxHRl-yT9yqmkEtRB6NCp9Zz59dWxUMZ3CGxKbk309YofrrzwN; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WhRxUJNnwCRss1GG4uj2WMJ; _s_tentry=passport.weibo.com; Apache=2885167477748.013.1761008832595; SINAGLOBAL=2885167477748.013.1761008832595; ULV=1761008832651:1:1:1:2885167477748.013.1761008832595:"}
def get_data(url):
    resp = requests.get(url, headers=h)
    resp.encoding = 'utf-8'
    tree = BeautifulSoup(resp.text, 'html.parser')
    data = tree.select('div.data > table > tbody > tr')
    resou_list = []
    for i in data:
        resou = i.select('td.td-02 > a')[0].get_text()
        link = i.select('td.td-02 > a')[0]['href']
        span_list = i.select('td.td-02 > span')
        #有的无span值，要加else不然会报错
        redu = span_list[0].get_text() if span_list else "无热度数据"  
        resou_list.append({'resou':resou,'link':link,'redu':redu})
    return resou_list
url='https://s.weibo.com/top/summary?cate=realtimehot'
resou_list1 = get_data(url)
def save_to_file(data, filename="hot_list.txt"):
    try:
        # 打开文件
        with open(filename, 'w', encoding='utf-8') as f:
            # 用json格式写入，确保中文正常显示，且格式化排版
            json.dump(data, f, ensure_ascii=False, indent=1)
        print(f"数据已成功保存到 {filename}")
    except Exception as e:
        print(f"保存文件失败：{e}")

# 调用函数保存数据
save_to_file(resou_list1)
