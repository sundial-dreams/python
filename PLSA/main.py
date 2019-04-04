import codecs
from math import *
from pylab import *


def read_file(filename: str):
    return codecs.open(filename, 'r', 'utf-8')


def main():
    # 读数据集
    documents = [document.strip() for document in read_file('dataset.txt')]

    # 文档总数
    N = len(documents)

    # topic数
    K = 10

    # 统计词语在每篇文档中的出现次数以及总词数

    # map类型，键是word，值是word在全部documents中出现的总次数
    word_count = {}

    # list类型，每个元素是一个map类型对象，键是word，值是word在对应的document中出现的次数
    word_count_per_document = []

    # 要去除的标点符号的正则表达式
    punctuation_regex = '[,.;"?!#-_…()`|“”‘]+'

    stopwords = ['a', 'an', 'after', 'also', 'they', 'man', 'zou', 'can', 'and', 'as', 'up', 'soon', 'be', 'being',
                 'but',
                 'by', 'd', 'for', 'from', 'he', 'her', 'his', 'in', 'is', 'more', 'of', 'often', 'the', 'to', 'who',
                 'with', 'people', 'or', 'it', 'that', 'its', 'are', 'has', 'was', 'on', 'at', 'have', 'into', 'no',
                 'which']

    for d in documents:
        words = d.split()
        word_count_current_doc = {}
        for w in words:
            # 过滤stopwords并小写化
            w = re.sub(punctuation_regex, '', w.lower())
            if len(w) <= 1 or re.search('http', w) or re.search('[0-9]', w) or w in stopwords:
                continue
            # 否则统计该词出现次数
            if w in word_count:
                word_count[w] += 1
            else:
                word_count[w] = 1
            if w in word_count_current_doc:
                word_count_current_doc[w] += 1
            else:
                word_count_current_doc[w] = 1
        word_count_per_document.append(word_count_current_doc)

    # 构造词表

    # map类型，键是word，值是word的编号
    dictionary = {}
    # map类型，键是word的编号，值是word
    dictionary_reverse = {}

    index = 0
    for word in word_count.keys():
        if word_count[word] > 1:
            dictionary[word] = index
            dictionary_reverse[index] = word
            index += 1

    # 词表长度
    M = len(dictionary)

    # 构造document-word矩阵

    X = zeros([N, M], int8)

    for word in dictionary.keys():
        j = dictionary[word]
        for i in range(0, N):
            if word in word_count_per_document[i]:
                X[i, j] = word_count_per_document[i][word]

    # 初始化参数

    # lambda0[i, j] : p(zj|di)
    lambda0 = random([N, K])
    for i in range(0, N):
        normalization = sum(lambda0[i, :])
        for j in range(0, K):
            lambda0[i, j] /= normalization

    # theta[i, j] : p(wj|zi)
    theta = random([K, M])
    for i in range(0, K):
        normalization = sum(theta[i, :])
        for j in range(0, M):
            theta[i, j] /= normalization

    # 定义隐变量的后验概率的矩阵表示

    # p[i, j, k] : p(zk|di,wj)
    p = zeros([N, M, K])

    # E-Step
    def e_step():
        for i in range(0, N):
            for j in range(0, M):
                denominator = 0
                for k in range(0, K):
                    p[i, j, k] = theta[k, j] * lambda0[i, k]
                    denominator += p[i, j, k]
                if denominator == 0:
                    for k in range(0, K):
                        p[i, j, k] = 0
                else:
                    for k in range(0, K):
                        p[i, j, k] /= denominator

    # M-Step
    def m_step():
        # 更新参数theta
        for k in range(0, K):
            denominator = 0
            for j in range(0, M):
                theta[k, j] = 0
                for i in range(0, N):
                    theta[k, j] += X[i, j] * p[i, j, k]
                denominator += theta[k, j]
            if denominator == 0:
                for j in range(0, M):
                    theta[k, j] = 1.0 / M
            else:
                for j in range(0, M):
                    theta[k, j] /= denominator

        # 更新参数lambda
        for i in range(0, N):
            for k in range(0, K):
                lambda0[i, k] = 0
                denominator = 0
                for j in range(0, M):
                    lambda0[i, k] += X[i, j] * p[i, j, k]
                    denominator += X[i, j]
                if denominator == 0:
                    lambda0[i, k] = 1.0 / K
                else:
                    lambda0[i, k] /= denominator

    def log_likelihood():
        log__likelihood = 0
        for i in range(0, N):
            for j in range(0, M):
                tmp = 0
                for k in range(0, K):
                    tmp += theta[k, j] * lambda0[i, k]
                if tmp > 0:
                    log__likelihood += X[i, j] * log(tmp)
        print('log likelihood : ', log__likelihood)

    # EM 算法 迭代20次
    log_likelihood()  # 顺便计算极大似然
    for i in range(0, 20):
        e_step()
        m_step()
        print("the", i + 1, "'s iteration  ")
        log_likelihood()

    topic_words = []
    max_topic_words_num = 10
    for i in range(0, K):
        topic_word = []
        ids = theta[i, :].argsort()
        for j in ids:
            topic_word.insert(0, dictionary_reverse[j])
        topic_words.append(topic_word[0:min(max_topic_words_num, len(topic_word))])

    for t in topic_words:
        print(t)


if __name__ == "__main__":
    main()
