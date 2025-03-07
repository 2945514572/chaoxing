import os
import pandas as pd


def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        try:
            if filename.endswith(".txt"):
                # 提取文件名的各个部分
                parts = filename.split("_")

                # 构建新的文件名
                new_filename = f"{parts[0]}_{parts[2]}_{parts[3]}.txt"

                # 构建文件的完整路径
                old_filepath = os.path.join(folder_path, filename)
                new_filepath = os.path.join(folder_path, new_filename)

                # 重命名文件
                os.rename(old_filepath, new_filepath)
        except:
            pass
    print("文件重命名完成。")

def delete_files_not_in_excel(folder_path, excel_file):
    # 读取Excel文件中的第一列值（股票代码）
    df = pd.read_excel(excel_file)
    stock_codes = df.iloc[:, 0].astype(str).tolist()
    print(stock_codes)
    # 遍历文件夹中的txt文件
    for filename in os.listdir(folder_path):
        try:
            if filename.endswith(".txt"):
                # 提取txt文件名的第一部分并转换为整数
                file_stock_code = str(int(filename.split("_")[0])).lstrip("0")
                # print(file_stock_code)
                # 如果txt文件名的第一部分不在股票代码列表中，则删除文件
                if file_stock_code not in stock_codes:
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)

                    print(f"已删除文件: {file_path}")
        except:
            pass

    print("文件删除完成。")


def add_extension_to_files(folder_path):
    for filename in os.listdir(folder_path):
        try:
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                new_filename = filename + ".txt"
                new_file_path = os.path.join(folder_path, new_filename)
                os.rename(file_path, new_file_path)
        except:
            pass
    print("文件重命名完成。")

def delete_files_with_keywords(folder_path, keywords):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            for keyword in keywords:
                if keyword in filename:
                    # try:
                    file_path = os.path.join(folder_path, filename)
                    os.remove(file_path)
                    print(f"已删除文件: {file_path}")
                    # except:
                    #     pass

if __name__ == "__main__":
    folder_path = "D:\\年报txt\\TXT版"  # 替换为实际的文件夹路径
    # folder_path = "E:/2011"
    # folder_path = "D:/BaiduNetdiskDownload/TXT版/TXT版"
    # rename_files_in_folder(folder_path)

    excel_file = "company.xlsx"  # 替换为实际的Excel文件路径
    # delete_files_not_in_excel(folder_path, excel_file)

    # add_extension_to_files(folder_path)

    # 指定要删除的关键词列表
    keywords = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "1999", "1998", "1997", "1996", "1995"]
    delete_files_with_keywords(folder_path, keywords)