from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time

# 设置Edge浏览器选项
edge_options = Options()
edge_options.use_chromium = True
edge_options.add_argument("--headless")  # 无头模式，不显示浏览器窗口

# 启动Edge浏览器
driver = webdriver.Edge(options=edge_options)

# 抖音直播间链接
live_url = 'https://www.douyin.com/?webRid=456066026839'

# 打开直播间链接
driver.get(live_url)

# 等待页面加载
time.sleep(5)

# 点击展开观众列表
expand_button = driver.find_element(By.XPATH, '//div[@class="room-actor-container"]')
expand_button.click()

# 模拟下滑操作，直到加载完所有在线观众
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 等待加载
    # 判断是否已加载完所有在线观众
    load_more_button = driver.find_elements(By.XPATH, '//div[@class="room-actor-container"]/div[@class="room-actor-more"]')
    if len(load_more_button) == 0:
        break

# 获取在线观众列表
audience_list = driver.find_elements(By.XPATH, '//div[@class="room-actor-container"]/div[@class="room-actor-list"]/div[@class="actor-info"]')

# 输出观众列表
for audience in audience_list:
    user_id = audience.find_element(By.XPATH, './/span[@class="room-actor-id"]').text
    nickname = audience.find_element(By.XPATH, './/span[@class="room-actor-name"]').text
    print(f'用户ID：{user_id}，昵称：{nickname}')

# 关闭浏览器
driver.quit()