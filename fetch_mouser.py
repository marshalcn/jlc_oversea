import random
import time

import requests
import json
import pymysql
import re


# 获取数据库连接 替换为自己的数据库连接
def get_db_connect():
    return pymysql.connect(host='aaaaaa.com', port=3306, user='root',
                           passwd='aaaaaaaaa', db='lc_oversea_product',
                           charset='utf8')


# 处理编码问题
common_db = get_db_connect()

# 请求头
header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'overseas.szlcsc.com',
        'referer': 'https://so.szlcsc.com/',        # 重要参数
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'cookie': 'cpx=1; Qs_lvt_290854=1630986062; Qs_pv_290854=1617424368694690300; acw_tc=6f06b41816309860598416291e7f1873e1fa583a980bdfc7e4d2cc3607',  # 重要参数，修改成自己的
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'  # 重要常见参数
    }


# 爬取物料信息 provider为Mouser Vertical等， pageNum 爬取数据的页码
def fetch_product_data(provider, pageNum):
    # 请求地址
    url = "https://overseas.szlcsc.com/overseas/global/search/mouser?callback=jQuery36005621381295033705_1630985411907" \
          "&keyword=&providers=" + provider + "&pageNumber=" + str(pageNum) + "&noShowSelf=false&_=1630985411929"
    # 发送请求
    response = requests.get(url, headers=header)
    # 正则去除首尾多余字符
    p = re.compile(r'[(](.*)[)]', re.S)
    result = re.findall(p, response.text)[0]
    # 将结果转为json对象
    js = json.loads(result)
    # 包装返回结果
    return {"result": js.get('result')[0].get('products'),
            "pageNumber": js.get('result')[0].get('pageNumber'),
            "pageTotal": js.get('result')[0].get('pageTotal'),
            "total": js.get('result')[0].get('total')}


# 存储爬取的数据，只保存部分主要数据
def persist_product_info(data):
    # 获取数据库连接
    db = get_db_connect()
    # 获取游标
    cursor = db.cursor()
    # 依次处理物料信息
    for item in data:
        try:
            # 提取有用信息
            catalog1 = fill_empty(item.get('catalog1'))
            provider = fill_empty(item.get('provider'))
            productCodeProvider = fill_empty(item.get('productCodeProvider'))
            productCodeManufacturer = fill_empty(item.get('productCodeManufacturer'))
            productCodeManufacturerHighlight = fill_empty(item.get('productCodeManufacturerHighlight'))
            productGradePlateName = fill_empty(item.get('productGradePlateName'))
            productGradePlateNameHighlight = fill_empty(item.get('productGradePlateNameHighlight'))
            stockNumber = str(item.get('stockNumber'))
            minBuyNumber = str(item.get('minBuyNumber'))
            productMinEncapsulationNumber = str(item.get('productMinEncapsulationNumber'))
            breviaryImageUrl = fill_empty(item.get('breviaryImageUrl'))
            bigImageUrl = fill_empty(item.get('bigImageUrl'))
            brandId = str(item.get('brandId'))
            brandName = fill_empty(item.get('brandName'))
            packaging = fill_empty(item.get('packaging'))
            detailUrl = fill_empty(item.get('detailUrl'))
            updateTime = fill_empty(item.get('updateTime'))
            eccn = fill_empty(item.get('eccn'))
            dataSheetUrl = fill_empty(item.get('dataSheetUrl'))
            # 拼接SQL语句
            sql = "INSERT INTO `lc_oversea_product`.`oversea_products`(`catalog1`, `provider`, `productCodeProvider`, `productCodeManufacturer`, `productCodeManufacturerHighlight`, `productGradePlateName`, `productGradePlateNameHighlight`, `stockNumber`, `minBuyNumber`, `productMinEncapsulationNumber`, `breviaryImageUrl`, `bigImageUrl`, `brandId`, `brandName`, `packaging`, `detailUrl`, `updateTime`, `eccn`, `dataSheetUrl`) VALUES (\'" + catalog1 + "\', \'" + provider + "\', \'" + productCodeProvider + "\', \'" + productCodeManufacturer + "\', \'" + productCodeManufacturerHighlight + "\', \'" + productGradePlateName + "\', \'" + productGradePlateNameHighlight + "\', " + stockNumber + ", " + minBuyNumber + ", " + productMinEncapsulationNumber + ", \'" + breviaryImageUrl + "\', \'" + bigImageUrl + "\', " + brandId + ", \'" + brandName + "\', \'" + packaging + "\', \'" + detailUrl + "\', \'" + updateTime + "\', \'" + eccn + "\', \'" + dataSheetUrl + "\');"
            print("----------------------------- FLUSH SQL -------------------------------")
            print(sql)
            # 执行并提交SQL
            cursor.execute(sql)
            db.commit()
            print("---------------------------- FLUSH OVER -------------------------------")
        except BaseException as e:
            print(item)
            print(e)
    db.close()


# 处理null值默认转为空字符串
def fill_empty(val):
    if val is None:
        return ""
    # 对字符串进行编码处理，防止特殊字符导致SQL语句出错
    return common_db.escape_string(val)


# 获取随机加时页间隔
def get_rand_page():
    rand_page_array = [7, 9, 10, 15, 8, 11, 6, 13]
    return rand_page_array[random.randint(0, len(rand_page_array) - 1)]


if __name__ == '__main__':
    provider = "mouser"
    page = 646
    # 拉取一次数据
    data = fetch_product_data(provider, page)
    totalPage = data.get("pageTotal")
    print('total:' + str(data.get("total")))
    print("totalPage:" + str(totalPage))
    # 保存拉取的数据
    persist_product_info(data.get("result"))
    # 随机间隔页
    rand_page = get_rand_page()
    # 随机间隔计数，每次间隔达到时置零
    rand_index = 0
    # 页面不到最终页一直执行
    while data.get("pageNumber") < data.get("pageTotal"):
        page = page + 1
        print("--------------------------- CURRENT PAGE [" + str(page) + "] START ----------------------------")
        print("--------------------------- RAND PAGE NUM [" + str(rand_page) + "] ----------------------------")
        # 休息一下，尽可能避免爬虫检测
        time.sleep(random.randint(9, 15))
        rand_index = rand_index + 1
        # 判断随机页是否到达，到达时触发休眠加时，并重置随机间隔计数，进一步避免爬虫检测
        if rand_index == rand_page:
            print("--------------------------- RELOAD RAND PAGE NUM START ----------------------------")
            rand_page = get_rand_page()
            rand_index = 0
            # 休眠加时，进一步避免爬虫检测
            time.sleep(random.randint(4, 9))
            print("--------------------------- RELOAD RAND PAGE NUM [" + str(rand_page) + "] OVER ----------------------------")
        # 异常处理，爬取失败后重试
        try:
            # 爬取数据
            data = fetch_product_data(provider, page)
            # 存储数据
            persist_product_info(data.get("result"))
        except BaseException as e:
            print(e)
            print("ERROR WHILE RESOLVE PAGE NUM %d" % page)
            page = page - 1
            print("READY TO RESET PAGE %d AND SLEEP FOR A WHILE" % page)
            time.sleep(random.randint(8, 16) * 100)
            data = {"pageNumber": page, "pageTotal": totalPage}

        print("--------------------------- CURRENT PAGE [" + str(page) + "] END ----------------------------")
