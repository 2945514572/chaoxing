import pandas as pd
import time

start_time = time.time()
df = pd.DataFrame()

for j in range(22, 23):
    try:
        for i in range(1, 400):
            url = f'https://s.askci.com/stock/a/0-0?reportTime=20{j}-12-31&pageNum={i}#QueryCondition'
            df = pd.concat([df, pd.read_html(url)[3].loc[:, :]])
            time.sleep(5)
            endtime = time.time() - start_time
            print('正在获取上市公司基本信息表第' + str(i) + '页', '已运行%.2f秒' % endtime)
    except:
        print('出错啦')
    df['股票代码'] = df['股票代码'].astype('str').str.zfill(6)
    df.drop(['序号', '招股书', '公司财报'], axis=1, inplace=True)

    # 筛选并删除行
    df = df[(df['城市'] == '上海市') | (df['城市'] == '深圳市')]

    filename = f'20{j}年上市公司基本信息表.xlsx'
    df.to_excel(filename, index=False)
    print('\n', '*******目标爬取完成*******')