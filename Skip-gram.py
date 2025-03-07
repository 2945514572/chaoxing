from gensim.models import Word2Vec
import jieba
import numpy as np
import os
from collections import defaultdict
import gensim
# 定义文件夹路径和文件扩展名
folder_path = 'D:/年报txt/TXT版'  # 文件夹路径
file_extension = '.txt'  # 文件扩展名
# 读取文件夹中的所有txt文件
file_paths = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(file_extension):
        file_paths.append(os.path.join(folder_path, file_name))
# 将文件内容转换为句子列表
sentences = []
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            words = jieba.lcut(line.strip())  # 使用jieba进行分词
            sentences.append(words)

# 训练Word2Vec模型
model = Word2Vec(sentences, sg=1, vector_size=300, window=5, min_count=5, hs=1, epochs=5, workers=4)

model.save("computer_model_1.model")
##########
# from gensim.models import Word2Vec
# # 训练Word2Vec模型，假设每台电脑的模型分别为computer_model_1、computer_model_2、computer_model_3
# computer_model_1 = Word2Vec(...)
# computer_model_2 = Word2Vec(...)
# computer_model_3 = Word2Vec(...)
# # 保存每台电脑的词向量模型
# computer_model_1.save("computer_model_1.model")
# computer_model_2.save("computer_model_2.model")
# computer_model_3.save("computer_model_3.model")
# #######
# model = gensim.models.Word2Vec.load('merged_model_0_1.bin')
# 加载种子词列表
# seed_words = []
# with open("D:/tools/Py代码/A股/模型/seed.txt", "r", encoding="utf-8") as file:
#     for line in file:
#         seeds = line.strip().split('\t')  # 使用制表符分割种子词
#         seed_words.extend(seeds)
# print("Seed words:", seed_words)  # 检查是否成功读取种子词列表
# # 计算种子词的相似词语
# similar_words = {}
# for seed_word in seed_words:
#     if seed_word in model.wv:
#         similar = model.wv.most_similar(seed_word, topn=10)
#         similar_words[seed_word] = [word for word, _ in similar]
#         print(seed_word)
#
# # 打印种子词及其相似词语
# for seed_word, similar in similar_words.items():
#     print(seed_word, similar)
# print("Vocabulary size:", len(model.wv))

# 种子词列表
# 加载种子词列表
seed_words = []
with open("D:/tools/Py代码/A股/模型/seed.txt", "r", encoding="utf-8") as file:
    for line in file:
        seeds = line.strip().split('\t')  # 使用制表符分割种子词
        seed_words.extend(seeds)

# 存储筛选结果的字典
similar_words = {}

# 遍历种子词
for seed_word in seed_words:
    # 存储与种子词最相似的词语及其相似度
    most_similar = []

    if seed_word in model.wv.key_to_index:
        # 获取种子词的向量
        seed_vector = model.wv.get_vector(seed_word)
        # print("Seed Vector shape:", seed_vector.shape)

        # 计算种子词与所有词的相似度
        similarities = model.wv.cosine_similarities(seed_vector.reshape(-1, 1), model.wv.vectors)


        # 遍历所有词语及其相似度
        for i, similarity in enumerate(similarities):
            word = model.wv.index_to_key[i]

            most_similar.append((word, similarity))

        # 按相似度降序排序并选取前10个
        most_similar.sort(key=lambda x: x[1][0], reverse=True)


        most_similar = most_similar[:10]

        # 将结果存入字典
        similar_words[seed_word] = most_similar
    else:
        # 如果词汇不存在，输出相应的提示或执行其他处理
        print("词汇 {} 不存在于模型的词汇表中。".format(seed_word))

# 打印结果
for seed_word, similar_list in similar_words.items():
    print("Seed Word:", seed_word)
    for word, similarity in similar_list:
        print(word, similarity)
    print()
output_file = "similar_words.txt"  # 输出文件路径

with open(output_file, "w", encoding="utf-8") as file:
    for seed_word, similar_list in similar_words.items():
        file.write("Seed Word: {}\n".format(seed_word))
        for word, similarity in similar_list:
            file.write("{} {}\n".format(word, similarity))
        file.write("\n")

print("结果已写入文件：", output_file)
