import requests
import os
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090c11)XWEB/11581',
    'Content-Type': 'application/json',
    'xweb_xhr': '1',
    'platform': 'wxMiniProgram',
    'type': 'windows',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://servicewechat.com/wx2cfd858ce50f552a/37/page-frame.html',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
json_data = {
    'id': '6404',
}
response = requests.post('https://xuexi.daanbest.com/addons/shopro/textbook.textbook/chapter', headers=headers, json=json_data)
print(response.text)
# 解析 JSON 响应
data = response.json()
# 提取图片链接
image_urls = data.get("data", {}).get("images", [])
# 创建文件夹存储图片
folder_path = "images"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
# 下载图片
for i, img_url in enumerate(image_urls):
    img_data = requests.get(img_url)
    if img_data.status_code == 200:
        img_name = f"image_{i+1}.jpg"
        img_path = os.path.join(folder_path, img_name)
        with open(img_path, 'wb') as f:
            f.write(img_data.content)
        print(f"图片 {img_name} 已保存。")
    else:
        print(f"图片 {img_url} 下载失败。")