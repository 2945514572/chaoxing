import requests
import json
i=0  #题目初始数量
a=0
a=int(a)
print('正在遍历,请耐心等待')
#最少48843最多59905
for keyword in range(48900,49001):
    a = a + 1
    if a%100==0:
        print('已遍历{}次！'.format(a))
    try:
        url = f"https://wx.jianankaopei.cn/app/index.php?i=7&t=0&v=1.0.14&from=wxapp&c=entry&a=wxapp&do=get_questions&state=we7sid-04920c2c26b163da28b666db613c92d8&sign=f02ce0124f9798df7efa70c0d79d167a&qid={keyword}&num=0&m=ck_onlinetest"
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36'}

        response = requests.get(url,headers=header)


        json_str = response.text
        json_sub_str = '\n'.join(json_str.splitlines())
        # 解析 JSON 对象
        json_obj = json.loads(json_sub_str)
        data= json_obj["data"]

        #处理题目
        title = data['title']
        q_type = data['type']
        content = data['content']
        options = data['option']
        correct_answers = data['correct_answer']
        id=data['id']
        content = data['content']

        with open('结果.txt', 'a', encoding='utf-8') as file:
            start_index = content.find('src="')
            i=i+1
            print("题目{}（ID: {}）：{}".format(i,id, title),file=file)

            if q_type == '1':
                question_type = '单选题'
            elif q_type == '2':
                question_type = '多选题'
            elif q_type == '3':
                question_type = '判断题'
            elif q_type == '4':
                question_type = '案例分析题'
            else:
                question_type = '未知题型'
            print("题目类型：", question_type, file=file)
            src_index = content.find('src="')
            if src_index != -1:
                start_index = content.find('src="') + 5
                end_index = content.find('"', start_index)
                a= content[start_index:end_index]
                print("题目材料图片链接：", a,file=file)
            elif q_type=="4":

                start_index = content.find('<p>') + 3
                end_index = content.find('</p>', start_index)
                a = content[start_index:end_index]
                print("案例材料：", a,file=file)
            else:
                q=0


            # print("选项：",file=file)

            if data['option']:
                file.write('选项：\n')
                for key, value in data['option'].items():
                    file.write( key + ': ' + value + '\n')
            # for option, value in options.items():
            #     print(option + ": " + value,file=file)
            print("答案：", correct_answers,file=file)
            file.write('\n')
            print("爬取到{}个题目!".format(i))
    except:
        pass
