import requests
import json
import re
from bs4 import BeautifulSoup
import time
from lxml import etree

url1="https://www.ke.com/city/"
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        }
res=requests.get(url1,headers=headers)
html = res.text
# 使用lxml解析HTML
tree = etree.HTML(html)
# 使用XPath定位元素
try:
    for p in range(1,10000):
        try:
            for i in range(1,10000):
                element = tree.xpath(f'/html/body/div[3]/div[2]/div[1]/div[2]/ul/li[{p}]/div[2]/div/ul/li[{i}]/a')
                href = element[0].get('href')
                text = element[0].text
                city = href.split('//')[1].split('.')[0]

                try:  #按页写入
                    with open(f'{text}.txt', 'w', encoding='utf-8') as file:
                        for q in range(1,50):
                            url=f"https://m.ke.com/{city}/jingjiren/ao12sy0pg{q}"
                            headers = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
                            }
                            res=requests.get(url,headers=headers)
                            # print(res.text)
                            html=res.text
                            soup = BeautifulSoup(html, 'html.parser')
                            script_tags = soup.find_all('script', type='text/javascript', charset='utf-8')

                            if len(script_tags) >= 4:
                                target_script = script_tags[3]
                                script_content = target_script.string
                                # print(script_content)
                                pass
                            else:
                                print("找不到第4个<script>标签")
                            pattern = r'window\.__PRELOADED_STATE__\s*=\s*(.*)'
                            # 在找到目标脚本后，修剪字符串为有效的JSON格式
                            script_content = target_script.string.strip()

                            # 处理可能存在的分号
                            if script_content.endswith(';'):
                                script_content = script_content[:-1]

                            match = re.search(pattern, script_content)

                            if match:
                                preloaded_state = match.group(1)
                                # print(preloaded_state)
                                pass
                            else:
                                print("未找到目标信息")
                            preloaded_state = json.loads(preloaded_state)
                            list_data = preloaded_state["jingjirenList"]["list"]
                            for i in range(0,30):
                                # print(list_data[i]["name"])
                                name=f'{list_data[i]["name"]}\n'
                                file.write(name)
                except:
                    pass
                print(text, "收录完毕")
                time.sleep(1)
        except:
            # print("城市")
            pass
except:
    print("结构")


# /html/body/div[3]/div[2]/div[1]/div[2]/ul/li[1]/div[2]/div/ul/li[1]/a
# /html/body/div[3]/div[2]/div[1]/div[2]/ul/li[1]/div[2]/div/ul/li[2]/a
