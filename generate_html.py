import os
import time

import pymysql


# 获取数据库连接 替换为自己的数据库连接
def get_db_connect():
    return pymysql.connect(host='aaaaaa.com', port=3306, user='root',
                           passwd='aaaaaaaaa', db='lc_oversea_product',
                           charset='utf8')


# 从数据库拉取信息
def fetch_data_from_db(page, limit):
    db = get_db_connect()
    sql = "SELECT bigImageUrl, productCodeManufacturer FROM oversea_products LIMIT " + str(page * limit) + "," + str(limit) + " ;"
    cursor = db.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


# 查询数据量
def get_product_table_info():
    db = get_db_connect()
    sql_count = "SELECT COUNT(*) FROM oversea_products;"
    cursor = db.cursor()
    cursor.execute(sql_count)
    return cursor.fetchone()


# 组装html文件
def generate_html(data, path, file_name):
    html_prefix = """<!DOCTYPE html>
                        <html>
                        <head>
                        <meta charset="UTF-8">
                        <style>
                        table{
                        border-collapse: collapse;
                        width: 100%;
                        }
                        th, td{
                        text-align: left;
                        padding: 8px;
                        }
                        tr:nth-child(even){
                        background-color: #fafafa;
                        }
                        th{
                        background-color: #7799AA;
                        color: white;
                        }
                        </style>
                        </head>
                        <body>
                        <table>
                        <tr><th>bigImageUrl</th><th>productCodeManufacturer</th></tr>"""
    html_body = ""
    html_foot = "</table></body></html>"
    for item in data:
        html_body = html_body + "<tr style='height:120px'><td style='height:120px'><img style='height:110px;transform:scale(0.7,0.7);' src='" + item[0] + "'></td><td>" + item[1] + "</td></tr>"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + file_name, 'w+', encoding='utf-8') as f:
        f.write(html_prefix + html_body + html_foot)


if __name__ == '__main__':
    # 生成html保存路径
    generate_folder = "f:\\data\\generate\\"
    # 生成html文件前缀
    file_name_prefix = "generate-"
    page = 0
    limit = 200
    total = get_product_table_info()[0]
    totalPage = 0
    if total % limit == 0:
        totalPage = total / limit
    else:
        totalPage = total // limit + 1
    print("total page: " + str(totalPage))
    for page in range(totalPage):
        print(page)
        result = fetch_data_from_db(page, limit)
        generate_html(result, generate_folder, file_name_prefix + str(page + 1) + "-" + str(limit) + ".html")
        time.sleep(3)
