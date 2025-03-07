from gensim.models import Word2Vec, KeyedVectors
import gensim
import os
import numpy
# from sklearn.metrics.pairwise import cosine_similarity
# 分布式训练，每台电脑独立训练模型
# ...

# 创建一个空的Word2Vec模型，用于存储合并后的词向量
total_model = Word2Vec(vector_size=300)

# 构建模型文件夹路径
model_folder = "D:/模型"

# 获取模型文件夹中的所有文件
files = os.listdir(model_folder)

# 存储所有模型的训练数据的列表
all_sentences = []

# 加载每个电脑的词向量模型并合并到总模型
for file in files:
    if file.endswith(".model"):
        # 加载词向量模型
        computer_model = Word2Vec.load(os.path.join(model_folder, file))
        # 提取模型的训练数据并添加到总列表中
        all_sentences.extend(computer_model.wv.index_to_key)

# 使用所有模型的原始训练数据构建并训练总模型
total_model.build_vocab(all_sentences)
total_model.train(all_sentences, total_examples=len(all_sentences), epochs=total_model.epochs)

# 保存合并后的总模型
total_model.save("total_model.bin")

# 最终得到的total_model即为整体的词向量模型，可以使用它进行后续的操作



# 加载已训练好的Word2Vec模型
model = gensim.models.Word2Vec.load('total_model.bin')
# 规范化词向量
model.wv.init_sims(replace=True)
# 种子词列表
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
    # print(model.wv.key_to_index)
    if seed_word in model.wv.key_to_index:
        # 如果存在，执行相似性计算或其他操作
        similarities = model.wv.cosine_similarities(model.wv['人工智能'].reshape(1, -1), model.wv.vectors)
        # 其他操作...

        # 遍历所有词语及其相似度
        for i, similarity in enumerate(similarities):
            word = model.wv.index2word[i]
            most_similar.append((word, similarity))

        # 按相似度降序排序并选取前10个
        most_similar.sort(key=lambda x: x[1], reverse=True)
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
# 打开输出文件并写入结果
with open(output_file, "w", encoding="utf-8") as file:
    for seed_word, similar_list in similar_words.items():
        file.write("Seed Word: {}\n".format(seed_word))
        for word, similarity in similar_list:
            file.write("{} {}\n".format(word, similarity))
        file.write("\n")

print("结果已写入文件：", output_file)