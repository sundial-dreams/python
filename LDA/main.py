import numpy as np
import time
import codecs
import jieba
import re

alpha = 5
beta = 0.1
iterationNum = 50
Z = []
K = 10


def read_file(filename: str): return codecs.open(filename, 'r', 'utf-8')


# 预处理(分词，去停用词，为每个word赋予一个编号，文档使用word编号的列表表示)
def pre_process():
    # 读取停止词文件
    stopwords = [line.strip() for line in read_file('stopwords.dic')]
    # 读数据集
    documents = [document.strip() for document in read_file('dataset.txt')]
    word_to_id = {}
    id_to_word = {}
    doc = []
    current_document = []
    current_word_id: int = 0

    for document in documents:
        # 分词
        seg_list = jieba.cut(document)
        for word in seg_list:
            word = word.lower().strip()
            # 单词长度大于1并且不包含数字并且不是停止词
            if len(word) > 1 and not re.search('[0-9]', word) and word not in stopwords:
                if word in word_to_id:
                    current_document.append(word_to_id[word])
                else:
                    current_document.append(current_word_id)
                    word_to_id[word] = current_word_id
                    id_to_word[current_word_id] = word
                    current_word_id += 1
        doc.append(current_document);
        current_document = []
    return doc, word_to_id, id_to_word


docs, word2id, id2word = pre_process()
N = len(docs)
M = len(word2id)
ndz = np.zeros([N, K]) + alpha
nzw = np.zeros([K, M]) + beta
nz = np.zeros([K]) + M * beta


# 初始化
def random_initialize():
    for d, doc in enumerate(docs):
        z_current_doc = []
        for w in doc:
            pz = np.divide(np.multiply(ndz[d, :], nzw[:, w]), nz)
            z = np.random.multinomial(1, pz / pz.sum()).argmax()
            z_current_doc.append(z)
            ndz[d, z] += 1
            nzw[z, w] += 1
            nz[z] += 1
        Z.append(z_current_doc)


# gibbs采样
def gibbs_sampling():
    # 为每个文档中的每个单词重新采样topic
    for d, doc in enumerate(docs):
        for index, w in enumerate(doc):
            z = Z[d][index]
            # 将当前文档当前单词原topic相关计数减去1
            ndz[d, z] -= 1
            nzw[z, w] -= 1
            nz[z] -= 1
            # 重新计算当前文档当前单词属于每个topic的概率
            pz = np.divide(np.multiply(ndz[d, :], nzw[:, w]), nz)
            # 按照计算出的分布进行采样
            z = np.random.multinomial(1, pz / pz.sum()).argmax()
            Z[d][index] = z
            # 将当前文档当前单词新采样的topic相关计数加上1
            ndz[d, z] += 1
            nzw[z, w] += 1
            nz[z] += 1


def perplexity():
    nd = np.sum(ndz, 1)
    n = 0
    ll = 0.0
    for d, doc in enumerate(docs):
        for w in doc:
            ll = ll + np.log(((nzw[:, w] / nz) * (ndz[d, :] / nd[d])).sum())
            n = n + 1
    return np.exp(ll / (-n))


def main():
    random_initialize()
    for i in range(0, iterationNum):
        gibbs_sampling()
        print(time.strftime('%X'), "Iteration: ", i, " Completed", " Perplexity: ", perplexity())

    topic_words = []
    max_topic_words_num = 10
    for z in range(0, K):
        ids = nzw[z, :].argsort()
        topic_word = []
        for j in ids:
            topic_word.insert(0, id2word[j])
        topic_words.append(topic_word[0: min(10, len(topic_word))])

    for t in topic_words:
        print(t)


if __name__ == "__main__":
    main()
