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
from src.languange_classifier.code_language_classifier import load_data, plot_graphs, soft_max, suffix
import src.languange_classifier.code_language_classifier as clc
from src.token_based_similarities.token_lcs import code2text
from tensorflow.keras.preprocessing.sequence import skipgrams
import xml.etree.ElementTree as ET
from src.ast_based_similarities.ast_similarities import parse_tree, traverse_and_parse, prefix
from src.ast_based_similarities.tree_node import Node
from src.ast_based_similarities.create_ast import create_ast
label = {
    "array":    [1, 0, 0, 0, 0],
    # "math":     [0, 1, 0, 0, 0, 0],
    "search":   [0, 1, 0, 0, 0],
    "sort":     [0, 0, 1, 0, 0],
    "string":   [0, 0, 0, 1, 0],
    "tree":     [0, 0, 0, 0, 1]
}

array_path = "../../data/leetcode/array"
# math_path = "../../data/leetcode/math"
search_path = "../../data/leetcode/search"
sort_path = "../../data/leetcode/array"
string_path = "../../data/leetcode/array"
tree_path = "../../data/leetcode/array"
raw_path = "../../data/leetcode/raw"

features = 1000
data_path = "../../data/leetcode"


def file_paths(data_path, language):
    ret = []
    for dirpath, dirnames, filenames in os.walk(data_path):
        for file in filenames:
            if file.endswith(suffix[language]):
                path = dirpath + "\\" + file
                # print(path)
                ret.append(path)
    return ret

def count():
    array = load_data(array_path, "java")
    # math = load_data(math_path, "java")
    search = load_data(search_path, "java")
    sort = load_data(sort_path, "java")
    string = load_data(string_path, "java")
    tree = load_data(tree_path, "java")
    raw = load_data(raw_path, "java")

    print(array.__len__())
    # print(math.__len__())
    print(search.__len__())
    print(sort.__len__())
    print(string.__len__())
    print(tree.__len__())
    print(raw.__len__())




def init_tokenizer():
    java_data = clc.load_data(data_path, "java")
    tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',)
    tokenizer.fit_on_texts(java_data)
    # save
    f = open('tokenizer_bow.pkl', 'wb')
    pickle.dump(tokenizer, f)
    f.close()


def init_node_tokenizer():
    paths = file_paths(data_path, "java")
    for p in paths:
        create_ast(p)
        print("creating xml in " + p)
    return




# 提取特征————词袋模型
# 单个文件
def get_feature_bag_of_word(path):
    f1 = open('tokenizer_bow.pkl', 'rb')
    tokenizer = pickle.load(f1)
    f1.close()
    code = code2text(path)
    seq = tokenizer.texts_to_sequences([code])[0]
    feature = [0] * features
    for i in range(seq.__len__()):
        if 0 < seq[i] < features:
            feature[seq[i]] += 1
    return feature


# 多个文件
def bag_of_word(path_list):
    ret = []
    for path in path_list:
        ret.append(get_feature_bag_of_word(path))
    return ret


# 提取特征————word embedding
def get_feature_word_embedding(path):
    # 使用bow的tokenizer
    f1 = open('tokenizer_bow.pkl', 'rb')
    tokenizer = pickle.load(f1)
    f1.close()
    code = code2text(path)
    seq = tokenizer.texts_to_sequences([code])[0]
    vocab_size = len(tokenizer.word_index)
    window_size = 2
    positive_skip_grams, _ = skipgrams(
        seq,
        vocabulary_size=vocab_size,
        window_size=window_size,
        negative_samples=0)

    return



def xml2tree(path):
    xml_file_tree = ET.parse(path)
    return xml_file_tree


pre_order = []
def preorder(root):
    # visiting
    pre_order.append(root.label)
    for child in root.children:
        preorder(child)
    return pre_order


def get_feature_ast_node_embedding(path):
    ast = xml2tree(path)
    (root, _) = parse_tree(ast)
    pre_order_path = preorder(root)
    pre_order = []




train_size = 50
def prepare_data():
    array = file_paths(array_path, "java")
    # math = file_paths(math_path, "java")
    search = file_paths(search_path, "java")
    sort = file_paths(sort_path, "java")
    string = file_paths(string_path, "java")
    tree = file_paths(tree_path, "java")
    raw = file_paths(raw_path, "java")

    X_train = bag_of_word(array[0: train_size] + search[0: train_size] + sort[0: train_size] + string[0: train_size] + tree[0: train_size])
    Y_train = [label["array"]] * train_size + [label["search"]] * train_size + [label["sort"]] * train_size + [label["string"]] * train_size + [label["tree"]] * train_size
    X_test = bag_of_word(array[train_size:] + search[train_size:] + sort[train_size:] + string[train_size:] + tree[train_size:])
    Y_test = [label["array"]] * (array.__len__() - train_size) + \
             [label["search"]] * (search.__len__() - train_size) + \
             [label["sort"]] * (sort.__len__() - train_size) + \
             [label["string"]] * (string.__len__() - train_size) + \
             [label["tree"]] * (tree.__len__() - train_size)

    x_train = np.array(X_train)
    x_test = np.array(X_test)
    y_train = np.array(Y_train)
    y_test = np.array(Y_test)
    raw_ = bag_of_word(raw)

    train_index = [i for i in range(x_train.__len__())]
    test_index = [i for i in range(x_test.__len__())]
    random.shuffle(train_index)
    random.shuffle(test_index)
    x_train = x_train[train_index]
    y_train = y_train[train_index]
    x_test = x_test[test_index]
    y_test = y_test[test_index]

    return (x_train, y_train), (x_test, y_test), raw_


def init_model():
    model = Sequential()
    model.add(Dense(input_dim=features, units=1000, activation='relu'))
    model.add(Dense(units=1000, activation='relu'))
    model.add(Dense(units=1000, activation='relu'))
    model.add(Dense(units=1000, activation='relu'))
    model.add(Dense(units=5, activation='softmax'))
    # set configurations
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def self_learning():
    (x_train, y_train), (x_test, y_test) , raw = prepare_data()
    model = init_model()
    # 一次确定多少个
    n = 1
    while raw:
        model.fit(x_train, y_train, batch_size=80, epochs=30,
            validation_data=(x_test, y_test), verbose=2)
        prediction = model.predict(raw)
        max_prediction = []
        for i in range(prediction.__len__()):
            max_prediction.append(max(prediction[i]))

        for i in range(n):
            if raw:
                index = max_prediction.index(max(max_prediction))
                data = np.array(raw[index])
                label = np.array(soft_max(prediction[index]))
                x_train = np.row_stack((x_train, data))
                y_train = np.row_stack((y_train, label))
                max_prediction.pop(index)
                raw.pop(index)
    model.save('function_classifier.h5')
    return model


if __name__ == "__main__":
    # get_feature_bag_of_word("../../data/test/java_file2.java")
    # count()
    # self_learning()

    # (x_train, y_train), (x_test, y_test) , raw = prepare_data()
    # model = init_model()
    # model.fit(x_train, y_train, batch_size=100, epochs=30,
    #       validation_data=(x_test, y_test), verbose=2)
    init_node_tokenizer()