from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


options = Options()
options.add_argument("--load-extension=C:/Users/LU/AppData/Local/Google/Chrome/User Data/Default/Extensions/jpbjcnkcffbooppibceonlgknpkniiff/3.0.992_0")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
time.sleep(1)
url = "https://i.chaoxing.com/base?fid=39375&wfworg=true&tid=0"
c=0
while True :
    try:
        driver.get(url)
        time.sleep(5)
        # 使用XPath定位器找到元素
        try:
            input_element = driver.find_element(By.XPATH, '//*[@id="phone"]')
            # 输入值
            input_element.send_keys("15855327395")                        #引号里面填账号
            time.sleep(1)
            input_element = driver.find_element(By.XPATH,'//*[@id="pwd"]')
            # 输入值
            input_element.send_keys("112233..332211")                     #引号里面填密码
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="loginBtn"]').click()   #登录
            time.sleep(5)
            driver.find_element(By.XPATH,'//a[@name="课程"]').click()
            time.sleep(3)

        except:
            pass
        # print(driver.page_source)
        # 切换到iframe的上下文
        driver.switch_to.frame("frame_content")
        # 获取iframe内的内容
        # 切回主页面的上下文
        # driver.switch_to.default_content()
        content = driver.page_source  #网页源码
        current_window_handle = driver.current_window_handle #窗口
        # 打印获取到的内容
        driver.find_element(By.XPATH, '//span[text()="统计计算与统计软件（英）"]').click()   #课程名
        time.sleep(5)
        # 获取所有窗口的句柄
        window_handles = driver.window_handles
        # 切换到新打开的标签页
        for window_handle in window_handles:
            if window_handle != current_window_handle:
                driver.switch_to.window(window_handle)
                break
        # 获取新标签页的内容
        new_page_content = driver.page_source
        driver.find_element(By.XPATH,'//*[@id="boxscrollleft"]/div/ul[1]/li[2]').click()
        time.sleep(5)

        driver.switch_to.frame("frame_content-zj")
        # driver.find_element(By.XPATH, '//*[@id="cur825380200"]').click()  ####点击第一个任务节点
        driver.find_element(By.XPATH, '//*[@id="cur822317091"]/div/div[3]/div').click()
        time.sleep(5)
        driver.switch_to.window(driver.window_handles[-1])
        span_elements = driver.find_elements(By.XPATH, '//span[@class="catalog_points_yi prevTips"]')  #子任务点
        span_num=len(span_elements)
        wait = WebDriverWait(driver, 60) #
        for i in range(len(span_elements)):
            # 使用CSS选择器查找符合条件的<div>元素
            driver.switch_to.window(driver.window_handles[-1])   #//*[@id="cur822317158"]/span[2]  //*[@id="cur822317159"]/span[2]
            span_elements = driver.find_elements(By.XPATH, '//span[@class="catalog_points_yi prevTips"]')
            # print(span_elements)
            # print(i)
            span_element = span_elements[i]
            parent_div = span_element.find_element(By.XPATH, '..')
            # 滚动到父<div>元素，使其可见
            driver.execute_script("arguments[0].scrollIntoView(true);", parent_div)
            parent_div.click()
            time.sleep(5)
            driver.switch_to.frame("iframe")
            # try:
            div_elements = driver.find_elements(By.CSS_SELECTOR, '.ans-job-icon.ans-job-icon-clear')#子任务点
            # 遍历每个<div>元素
            for div_element in div_elements:
                # 获取aria-label属性的值
                aria_label = div_element.get_attribute('aria-label')
                # 比较aria-label的值
                if aria_label == '任务点未完成':
                    parent_div = div_element.find_element(By.XPATH, '..')
                    driver.execute_script("arguments[0].scrollIntoView();", parent_div)
                    time.sleep(2)
                    # 执行点击操作
                    parent_div.click()
                    wait_time = 60
                    # # 每分钟检查一次，直到'aria-label'的值为"任务点已完成"
                    while True:
                        try:
                            time.sleep(3)
                            wait.until(lambda driver: div_element.get_attribute('aria-label') == '任务点已完成')
                            time.sleep(3)
                            break  # 跳出循环
                        except:
                            pass

                else:
                    continue
                print("完成1个视频任务点")
        print("完成所有视频任务点")
        break
    except :
        c = c + 1
        if c > 10:
            break
        time.sleep(2)
        pass

# time.sleep(1000)