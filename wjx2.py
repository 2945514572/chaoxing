import logging
import random
import selenium
import re
import traceback
from threading import Thread
import time
from selenium.webdriver.support.ui import WebDriverWait
import numpy as np
import requests
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.wjx.cn/vm/PD75YHa.aspx#"


def wait_for_element(driver, selector):
    wait = WebDriverWait(driver, 10)  # 设置最大等待时间为10秒
    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    return element


# 校验IP地址合法性
def validate(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(\d{1,5})$'
    if re.match(pattern, ip):
        return True
    return False


# 检测题量和页数的函数，返回一个列表，第一个数表示第一页的题量，第二个数表示第二页的题量；比如示例问卷会返回：[3, 2, 2, 7]
# 虽然但是，我见识过问卷星再没有跳题逻辑的情况下有题被隐藏，我当时就??????
# 这会导致detect返回包含被隐藏的题，数值可能偏高，比如可见题目[3, 2, 2, 7]被detect成[4, 2, 2, 7]。。
def detect(driver):
    q_list = []  # 长度等于页数，数字代表该页的题数
    xpath = '//*[@id="divQuestion"]/fieldset'
    page_num = len(driver.find_elements(By.XPATH, xpath))  # 页数
    qs = driver.find_elements(By.XPATH, f'//*[@id="fieldset1"]/div')  # 每一页的题
    invalid_item = 0  # 无效问题数量
    for qs_item in qs:
        # 判断其topic属性值是否值包含数字
        if qs_item.get_attribute("topic").isdigit() is False:
            invalid_item += 1
    # 如果只有1页
    q_list.append(len(qs) - invalid_item)
    if page_num >= 2:
        for i in range(2, page_num + 1):
            qs = driver.find_elements(By.XPATH, f'//*[@id="fieldset{i}"]/div')
            invalid_item = 0  # 每一页的无效问题初始值为0
            # 遍历每一个div，判断其是否可以回答
            for qs_item in qs:
                # 判断其topic属性值是否值包含数字，因为只有题的div的topic属性才是纯数字
                if qs_item.get_attribute("topic").isdigit() is False:
                    invalid_item += 1
            # [3, 2, 2, 7]
            q_list.append(len(qs) - invalid_item)
    return q_list

from selenium.webdriver.common.by import By

# 提取矩阵题和量表题数量及每题选项数目
def extract_question_data(driver):
    # 提取矩阵题数量和每题选项数量
    matrix_xpath = '//*[@id="divRefTab"]//tbody/tr'  # 矩阵题的行
    matrix_questions = driver.find_elements(By.XPATH, matrix_xpath)
    matrix_count = 0
    matrix_options_count = []

    for tr in matrix_questions:
        if tr.get_attribute("rowindex") is not None:
            matrix_count += 1
            # 获取矩阵题的选项数量
            options_xpath = f'//*[@id="drv1_1"]/td'  # 示例，可能需要根据不同情况动态生成
            options = driver.find_elements(By.XPATH, options_xpath)
            matrix_options_count.append(len(options))

    # 提取量表题数量和每题选项数量
    scale_xpath = '//*[@id="div"]/div[2]/div/ul/li'  # 量表题的选项
    scale_questions = driver.find_elements(By.XPATH, scale_xpath)
    scale_count = 0
    scale_options_count = []

    for scale in scale_questions:
        scale_count += 1
        options_xpath = f'//*[@id="div{scale.get_attribute("id")}"]/div/ul/li'  # 动态生成量表题的选项
        options = driver.find_elements(By.XPATH, options_xpath)
        scale_options_count.append(len(options))

    # 返回矩阵题和量表题数量及每题选项数量
    return matrix_count, matrix_options_count, scale_count, scale_options_count

# 调用函数并打印结果
matrix_count, matrix_options_count, scale_count, scale_options_count = extract_question_data(driver)
print(f"矩阵题数量: {matrix_count}")
print(f"矩阵题选项数量: {matrix_options_count}")
print(f"量表题数量: {scale_count}")
print(f"量表题选项数量: {scale_options_count}")

# 矩阵题处理函数
def matrix(driver, current, index):
    xpath1 = f'//*[@id="divRefTab{current}"]/tbody/tr'
    a = driver.find_elements(By.XPATH, xpath1)
    q_num = 0  # 矩阵的题数量
    for tr in a:
        if tr.get_attribute("rowindex") is not None:
            q_num += 1
    # 选项数量
    xpath2 = f'//*[@id="drv{current}_1"]/td'
    options = driver.find_elements(By.XPATH, xpath2)  # 题的选项数量+1 = 6
    # 遍历每一道小题
    for i in range(1, q_num + 1):
        # p = matrix_prob[index]
        # index += 1
        # if p == -1:
        #     opt = random.randint(2, len(b))
        # else:
        #     opt = np.random.choice(a=np.arange(2, len(b) + 1), p=p)
        mean = len(options) // 2
        std_dev = len(options) // 4
        # 生成符合正态分布的随机数，并将其限制在选项的索引范围内
        random_index = int(round(np.random.normal(loc=mean, scale=std_dev)))
        random_index = max(2, min(len(options), random_index))
        driver.find_element(By.CSS_SELECTOR, f'#drv{current}_{i} > td:nth-child({random_index})').click()
    return index


# 量表题处理函数
# def scale(driver, current, index):
#     xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
#     a = driver.find_elements(By.XPATH, xpath)
#     p = scale_prob[index]
#     if p == -1:
#         b = random.randint(1, len(a))
#     else:
#         b = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
#     driver.find_element(By.CSS_SELECTOR,
#                         f"#div{current} > div.scale-div > div > ul > li:nth-child({b})").click()
# 量表题处理函数
def scale(driver, current):
    xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
    options = driver.find_elements(By.XPATH, xpath)

    # 计算正态分布的均值和标准差
    mean = len(options) // 2
    std_dev = len(options) // 4
    # 生成符合正态分布的随机数，并将其限制在选项的索引范围内
    random_index = int(round(np.random.normal(loc=mean, scale=std_dev)))
    random_index = max(1, min(len(options), random_index))
    # 点击选定的选项
    driver.find_element(By.CSS_SELECTOR,
                        f"#div{current} > div.scale-div > div > ul > li:nth-child({random_index})").click()


# 刷题逻辑函数
def brush(driver):
    q_list = detect(driver)  # 检测页数和每一页的题量
    single_num = 0  # 第num个单选题
    vacant_num = 0  # 第num个填空题
    droplist_num = 0  # 第num个下拉框题
    multiple_num = 0  # 第num个多选题
    matrix_num = 0  # 第num个矩阵小题
    scale_num = 0  # 第num个量表题
    current = 0  # 题号
    for j in q_list:  # 遍历每一页
        for k in range(1, j + 1):  # 遍历该页的每一题
            current += 1
            # 判断题型 md, python没有switch-case语法
            q_type = driver.find_element(By.CSS_SELECTOR, f'#div{current}').get_attribute("type")
            if q_type == "5":  # 量表题
                try:
                    # scale(driver, current, scale_num)
                    scale(driver, current)
                    time.sleep(0.1)
                except:
                    pass
                scale_num += 1
            elif q_type == "6":  # 矩阵题
                # try:
                matrix_num = matrix(driver, current, matrix_num)
                time.sleep(0.1)
                # except:
                #     pass
            elif q_type == "8":  # 滑块题
                try:
                    score = random.randint(1, 100)
                    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(score)
                    time.sleep(0.1)
                except:
                    pass

            else:
                print(f"第{k}题为不支持题型！")
        time.sleep(0.5)
        #  一页结束过后要么点击下一页，要么点击提交
        try:
            driver.find_element(By.CSS_SELECTOR, '#divNext').click()  # 点击下一页
            time.sleep(0.5)
        except:
            # 点击提交
            wait = WebDriverWait(driver, 3)  # 最多等待10秒钟
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctlNext"]')))
            next_button.click()
            # driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    submit(driver)


# 提交函数
def submit(driver):
    time.sleep(1)
    # 点击对话框的确认按钮
    try:
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        time.sleep(1)
    except:
        pass
    # 点击智能检测按钮，因为可能点击直接提交过后提交成功的情况，所以智能检测也要try
    try:
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(3)
    except:
        pass

    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size['width']
            # print(width)
            ActionChains(driver).drag_and_drop_by_offset(slider, width - 25, 0).perform()
    except selenium.common.exceptions.NoSuchElementException:
        # time.sleep(1000)
        pass


def run(xx, yy):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    option.add_argument('--headless')
    global count
    global stop
    global fail  # 失败次数
    while not stop:
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(550, 650)
        driver.set_window_position(x=xx, y=yy)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
        try:
            while True:
                driver.get(url)
                time.sleep(1)
                url1 = driver.current_url  # 表示问卷链接
                brush(driver)
                # 刷完后给一定时间让页面跳转
                time.sleep(4)
                url2 = driver.current_url  # 表示问卷填写完成后跳转的链接，一旦跳转说明填写成功
                if url1 != url2:
                    count += 1
                    print(f"已填写{count}份 - 失败{fail}次 - {time.strftime('%H:%M:%S', time.localtime(time.time()))} ")
                    # driver.quit()
                    time.sleep(1)
        except:
            traceback.print_exc()
            fail += 1
            logging.warning(f"已失败{fail}次,失败超过10次(左右)将强制停止------------------------------")
            if fail >= 10000:  # 失败阈值
                stop = True
                logging.critical('失败次数过多，为防止耗尽ip余额，程序将强制停止，请检查代码是否正确')
                quit()
            # time.sleep(1000)
            driver.quit()
            continue


# # 多线程执行run函数
# if __name__ == "__main__":
#     count = 0  # 记录已刷份数
#     fail = 0  # 失败次数
#     useIp = False  # useIp变量，是我为这个程序做的最极致的优化（2023.12.09）
#     stop = False
#
#     # 需要几个窗口同时刷就设置几个thread_?，默认两个，args里的数字表示设置浏览器窗口打开时的初始xy坐标
#     thread_1 = Thread(target=run, args=(50, 50))
#     thread_2 = Thread(target=run, args=(650, 50))
#     thread_3 = Thread(target=run, args=(650, 280))
#
#     thread_1.start()
#     thread_2.start()
#     thread_3.start()
#
#     thread_1.join()
#     thread_2.join()
#     thread_3.join()
