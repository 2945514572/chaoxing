import pandas as pd
import glob

# 获取所有 Excel 文件的文件路径
file_paths = glob.glob('D:/tools/Py代码/A股/公司信息/*.xlsx')

# 创建一个空 DataFrame，用于存储最终结果
result_df = pd.DataFrame(columns=['股票代码', '股票简称'])

# 读取第一个 Excel 文件的第一列和第二列数据，作为初始结果
first_file_path = file_paths[0]
first_df = pd.read_excel(first_file_path)
result_df['股票代码'] = first_df['股票代码']
result_df['股票简称'] = first_df.iloc[:, 1]

# 遍历剩余的 Excel 文件，保留在第一列中存在的值所在的行，并更新第二列的数据
for file_path in file_paths[1:]:
    df = pd.read_excel(file_path)
    result_df = result_df[result_df['股票代码'].isin(df['股票代码'])]
    result_df['股票简称'] = result_df['股票代码'].map(df.set_index('股票代码')['股票简称'])

# 保存结果为新的 Excel 文件
result_df.to_excel('output.xlsx', index=False)