import os
import pickle
import random
import re
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model
from keras.utils import plot_model


# 使用神经网络进行代码语言分类

# 代码文件数量：
# python: 3272
# java: 1556
# js: 2099
# c&cpp: 1570
# 每种语言取1000份代码作为训练集，500份代码作为验证集
java_path = "../../data/java"
python_path = "../../data/python"
js_path = "../../data/javascript"
ccpp_path = "../../data/c&cpp"
test_path = "../../data/test"

# 代码语言的后缀名
suffix = {
    "java": ".java",
    "python": ".py",
    "javascript": ".js",
    "xml": ".xml",
    "c": ".c",
    "cpp": ".cpp"
}

# 代码语言的标签(one-hot)
label = {
    "java": [1, 0, 0, 0],
    "python": [0, 1, 0, 0],
    "js": [0, 0, 1, 0],
    "ccpp": [0, 0, 0, 1]
}

# 每个语言的训练集大小和测试集大小
training_size = 1000
testing_size = 500

# 分类语言数量
N = 4


# 返回data_path下所有代码文件的字符串
def load_data(data_path, language):
    ret = []
    for dirpath, dirnames, filenames in os.walk(data_path):
        for file in filenames:
            if file.endswith(suffix[language]):
                path = dirpath + "\\" + file
                # print(path)
                text = open(path, encoding='UTF-8').read()
                # 删除换行符和tab
                # text = text.replace("\n", ""). replace("\t", "")
                # 删除注释
                # text = re.sub("(?:/\\*(?:[^*]|(?:\\*+[^*/]))*\\*+/)|(?://.*)", '', text)

                text = add_blank(text)
                ret.append(text)
    return ret


# 在特殊字符前后加空格
def add_blank(text):
    text = re.sub(";", " ; ", text)
    text = re.sub("#", " # ", text)
    text = re.sub("//", " // ", text)
    # text = re.sub("{", " { ", text)
    # text = re.sub("}", " } ", text)
    return text


# 取前1000个词
max_length = 1000
# 取1000个特征
features = 1000


# 用来处理代码文件转成能使用的特征
# 想法：用频率最高的1000个词作为1000维特征(是否可行？
# 看起来可行！
def prepare_data():
    # load data
    java_data = load_data(java_path, "java")
    python_data = load_data(python_path, "python")
    js_data = load_data(js_path, "javascript")
    ccpp_data = load_data(ccpp_path, "c") + load_data(ccpp_path, "cpp")

    # slice data
    train_data = java_data[0: training_size] + python_data[0: training_size] + js_data[0: training_size] + ccpp_data[0: training_size]
    test_data = java_data[training_size: training_size + testing_size] + \
                python_data[training_size: training_size + testing_size] + \
                js_data[training_size: training_size + testing_size] + \
                ccpp_data[training_size: training_size + testing_size]

    # label:
    train_label = [label["java"]] * training_size + [label["python"]] * training_size + [label["js"]] * training_size + [label["ccpp"]] * training_size
    test_label = [label["java"]] * testing_size + [label["python"]] * testing_size + [label["js"]] * testing_size + [label["ccpp"]] * testing_size

    y_train = np.array(train_label)
    y_test = np.array(test_label)

    # init tokenizer
    # train_tokenizer = tokenize(train_data)

    # save tokenizer
    # f = open('tokenizer.pkl', 'wb')
    # pickle.dump(train_tokenizer, f)
    # f.close()

    # read tokenizer
    f1 = open('tokenizer.pkl', 'rb')
    train_tokenizer = pickle.load(f1)
    f1.close()

    # 从string变成int数组
    train_sequences = train_tokenizer.texts_to_sequences(train_data)
    test_sequences = train_tokenizer.texts_to_sequences(test_data)

    train_sequences = pad_sequences(train_sequences, padding='post', truncating='post', maxlen=max_length)
    test_sequences = pad_sequences(test_sequences, padding='post', truncating='post', maxlen=max_length)

    x_train = np.empty([N * training_size, features], "int")
    for i in range(train_sequences.__len__()):
        for j in range(max_length):
            if 0 < train_sequences[i][j] <= features:
                tmp = train_sequences[i][j]
                x_train[i][tmp] = 1

    x_test = np.empty([N * testing_size, features], "int")
    for i in range(test_sequences.__len__()):
        for j in range(max_length):
            if 0 < test_sequences[i][j] <= features:
                tmp = test_sequences[i][j]
                x_test[i][tmp] = 1

    # 随机化
    train_index = [i for i in range(N * training_size)]
    test_index = [i for i in range(N * testing_size)]
    random.shuffle(train_index)
    random.shuffle(test_index)
    x_train = x_train[train_index]
    y_train = y_train[train_index]
    x_test = x_test[test_index]
    y_test = y_test[test_index]

    return (x_train, y_train), (x_test, y_test)


# 初始化神经网络
def init_model():
    # define network structure
    model = Sequential()
    model.add(Dense(input_dim=features, units=1000, activation='relu'))
    model.add(Dense(units=200, activation='relu'))
    model.add(Dense(units=4, activation='softmax'))
    # set configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer='adagrad',
                  metrics=['accuracy'])
    return model


# 计算代码文件数量
def count():
    py = load_data(python_path, "python")
    js = load_data(js_path, "javascript")
    java = load_data(java_path, "java")
    ccpp = load_data(ccpp_path, "c") + load_data(ccpp_path, "cpp")
    print("python:", py.__len__())
    print("java:", java.__len__())
    print("js:", js.__len__())
    print("ccpp:", ccpp.__len__())


# 画画
def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_'+string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_'+string])
    plt.show()


def tokenize(data):
    # init tokenizer
    tokenizer = Tokenizer(num_words=1000,
                          filters='!"$%&()*+,-./:<=>?@[\\]^_`|{}~\t\n')  # 去掉了可能能够分别语言的符号
    tokenizer.fit_on_texts(data)
    return tokenizer


# 用来将一个文本文件转换成上述特征向量
def handle_user_data(path):
    text = [open(path, encoding='UTF-8').read()]
    text[0] = add_blank(text[0])
    # read tokenizer
    f1 = open(os.path.dirname(os.path.realpath(__file__)) + "\\\\" +'tokenizer.pkl', 'rb')
    tokenizer = pickle.load(f1)
    f1.close()

    sequence = tokenizer.texts_to_sequences(text)
    sequence = pad_sequences(sequence, padding='post', truncating='post', maxlen=max_length)
    feature = np.zeros([1, features], "int")
    for j in range(max_length):
        tmp = sequence[0][j]
        if 0 < sequence[0][j] <= features:
            feature[0][tmp] = 1
        else:
            feature[0][tmp] = 0
    return feature


# 训练并保存模型
def train():
    (x_train, y_train), (x_test, y_test) = prepare_data()
    model = init_model()
    model.summary()
    history = model.fit(x_train, y_train, batch_size=50, epochs=60,
              validation_data=(x_test, y_test), verbose=2)
    plot_graphs(history, "accuracy")
    plot_graphs(history, "loss")

    model.save('language_classifier.h5')


def one_hot(arr):
    max1 = max(arr)
    ret = []
    for i in arr:
        if i == max1:
            ret.append(1)
        else:
            ret.append(0)
    return ret


def predict(path):
    model = load_model(os.path.dirname(os.path.realpath(__file__)) + "\\\\" +'language_classifier.h5')
    # model.summary()
    # plot_model(model, to_file='model.png')
    test = handle_user_data(path)
    prediction = model.predict(test)
    tmp = prediction[0]
    int_tmp = one_hot(tmp)
    lang = ""
    if int_tmp == label["java"]:
        lang = "java"
    elif int_tmp == label["python"]:
        lang = "python"
    elif int_tmp == label["js"]:
        lang = "javascript"
    elif int_tmp == label["ccpp"]:
        lang = "c&cpp"
    print("predict language:", lang)
    print("prossibility: ", max(tmp))
    return lang, max(tmp)


if __name__ == "__main__":
    train()
    # count()
    predict('./code_language_classifier.py')
    predict('../../data/test/java_file1.js')
    predict('../../data/test/java_file2.java')
    predict('../../data/test/js_file1.java')
    predict('../../data/test/js_file2.js')
    predict('../../data/test/python_file1.java')
    predict('../../data/test/python_file2.js')
    predict('../../data/test/ccpp_file1.cpp')
