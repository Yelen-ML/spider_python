import requests
import json
import pymysql
def get_data(url):
    response = requests.get(url)
    for i in response.json()['Data']['Posts']:
        yield i['RecruitPostName'], i['CountryName'], i['LocationName']
key=input("请输入搜索关键字：")
urls=['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1760278307296&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(key,i) for i in range(11)]
db_config = {
    "host": "192.168.80.128",    
    "user": "root",         
    "password": "123456", 
    "database": "recruit", 
    "charset": "utf8mb4"     
}

try:
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()  


    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tencent_jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        recruit_post_name VARCHAR(255) NOT NULL,  
        country_name VARCHAR(50) NOT NULL,     
        location_name VARCHAR(50) NOT NULL    
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_table_sql)
    conn.commit()

   
    total = 0  
    for url in urls:
        for job in get_data(url):
            if not all(job):
                continue
            insert_sql = """
            INSERT INTO tencent_jobs (recruit_post_name, country_name, location_name)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_sql, job)
            total += 1
    conn.commit()  # 批量提交
    print(f"数据存储完成，共插入 {total} 条记录")

except pymysql.Error as e:
    print(f"数据库错误：{e}")
    if 'conn' in locals():
        conn.rollback()  
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("数据库连接已关闭")
    