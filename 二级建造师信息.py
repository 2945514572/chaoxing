import json
import requests
import pandas as pd
import time


# 读取 Excel 姓名 文件
df = pd.read_excel("11.xlsx")     ######此处填写储存姓名的EXCEL文件地址！！！（例如：E://name.xlsx）###


# 去重
df = df.drop_duplicates()
# 将去重后的数据写到新文件中，第一行不包括列名
df.to_excel("name.xlsx", index=False, header=['name'])
# 读取Excel表格数据
df = pd.read_excel('name.xlsx')
# 获取关键字列数据
keywords = df['name'].tolist()
print(keywords)
# 遍历关键字列表并搜索每个关键字

for keyword in keywords:
    try:
        url=f"http://api.zhitaosoft.com/dzzz/appSearch.do?type=C001&status=&condition=1&content={keyword}"
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36'}
        res=requests.get(url,headers=header)
        #设置延时，缓解服务器压力
        # time.sleep(2)
        #解析json数据
        json_str = res.text
        json_sub_str = '\n'.join(json_str.splitlines())
        # 解析 JSON 对象
        json_obj = json.loads(json_sub_str)
        f = json_obj["resultJson"]  # json第一人信息
        for i in f:
            ls = []
            ls.append(i['A0101'])
            ls.append(i['A0106'])
            ls.append(i['A0104'])
            ls.append(i['A0116'])
            ls.append(i['A0128'])
            ls.append(i['A0133'])
            ls.append(i['a0100'])
            # print(ls)
            with open('output.txt', mode='a', encoding='utf-8') as file:
                file.write('\t'.join(ls) + '\n')
                print("成功爬取{:^5}信息".format(keyword))
    except:
        print("爬取{:^5}信息失败".format(keyword))