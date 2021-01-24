import os
import src.languange_classifier.code_language_classifier as clc
from tensorflow.python.keras.models import load_model
import pickle
import numpy as np
import re
import src.ast_based_similarities.create_ast as ast_creator
from tensorflow.keras.preprocessing.sequence import pad_sequences
import src.function_classifier.code_function_classifier_cpp as cfc_cpp
import src.function_classifier.code_function_classifier as cfc
import src.ast_based_similarities.ast_similarities as ast_evaluator
import src.token_based_similarities.token_lcs as token
import src.token_based_similarities.token_lcs_cpp as token_cpp
import src.quality_evaluator.code_smell_detector as quality_evaluator

data_path_dict = {"java" : os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "\\\\" + "..\\\\..\\\\data\\\\leetcode"),
                      "c&cpp" : os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "\\\\" + "..\\\\..\\\\data\\\\leetcode_cpp")
                      }

func_model= {"java" : cfc,
                  "c&cpp" : cfc_cpp
}

token_sim = {"java": token,
             "c&cpp" : token_cpp
             }

recommend_threshold = 5

# text_threshold = 0.50

def recommend_code(source_text):
    tmp_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "input_code_file"), 'input_file')
    creat_file(tmp_path + '.txt', source_text)
    lang,lan_prob = clc.predict(tmp_path + '.txt')
    # 消除文本文件
    os.remove(tmp_path + '.txt')

    if lang in func_model.keys():
        new_file = tmp_path + '.' + lang
        # 特判c&cpp
        if new_file.endswith(".c&cpp"):
            new_file = new_file[0: new_file.rfind('.')] + '.cpp'
        #

        creat_file(new_file, source_text)
        func, func_prob = predict_function(new_file, lang)
        ast_creator.create_ast(new_file)

        xml_file = tmp_path + '.xml'

        func_path = get_func_path(func, lang)
        text_sim_list = get_recommend_list_token(func_path, new_file, lang)
        # top_three_ast = get_top_three_ast_sim(text_sim_list, xml_file)
        top_three = get_top_three(text_sim_list)
        return top_three
    else:
        return "Sorry, we can't recommend code for you"


def get_lang(text):
    tmp_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "input_code_file"), 'input_file')
    creat_file(tmp_path + '.txt', text)
    lang, lan_prob = clc.predict(tmp_path + '.txt')
    os.remove(tmp_path + '.txt')
    return lang, lan_prob
# 相似度权重 0.75 质量权重 0.25
def get_top_three(text_sim_list):
    new_list = []
    for l in text_sim_list:
        tmp_list = []
        tmp_list.append(l[0])
        tmp_list.append(l[1])
        tmp_list.append(l[2])
        tmp_list.append(l[3])
        avg = l[2] * 100 * 0.75 + l[3] *0.25
        tmp_list.append(avg)
        new_list.append(tmp_list)
    new_list = sorted(new_list, key=lambda d: d[2], reverse=True)
    top_three = []
    for i in range(len(new_list)):
        if i < 3:
            top_three.append(new_list[i])
        else:
            break

    return top_three
def get_func(text):
    tmp_path = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "input_code_file"), 'input_file')
    creat_file(tmp_path + '.txt', text)
    lang,lan_prob = clc.predict(tmp_path + '.txt')
    # 消除文本文件
    os.remove(tmp_path + '.txt')

    if lang == 'python':
        return None, None

    new_file = tmp_path + '.' + lang
    # 特判c&cpp
    if new_file.endswith(".c&cpp"):
        new_file = new_file[0: new_file.rfind('.')] + '.cpp'

    creat_file(new_file, text)
    func, func_prob = predict_function(new_file, lang)
    return func, func_prob


def get_recommend_list_token(func_path, file, language_label):
    sim_dict = {}
    lang = file[file.rfind('.')+1:]
    paths = cfc.file_paths(func_path, lang)
    for path in paths:
        ans = token_sim[language_label].token_lcs(path, file)
        sim_dict[path] = ans
    sim_dict = sorted(sim_dict.items(), key=lambda d: d[1], reverse=True)

    recommend_list = list()
    for tuple in sim_dict:
        tmp_list = list()
        path = tuple[0]
        code_path = path[0:path.rfind('\\')]
        file_name = path[path.rfind('\\')+1:]
        score = quality_evaluator.average_score(code_path, file_name)
        tmp_list.append(file_name)
        tmp_list.append(token.code2text(path))
        tmp_list.append(tuple[1]) #相似度
        tmp_list.append(score)
        recommend_list.append(tmp_list)
    return recommend_list


def get_top_three_ast_sim(sim_list, xml_file):
    list = []
    for i in range(len(sim_list)):
        path = sim_list[i][0]
        if i < 3 :
            xml_path = cfc.code_path2xml_path(path)
            ans = ast_evaluator.tree_distance_similarities(xml_path, xml_file)
            list.append(ans)
            print(ans)
        else:
            break
    return list



def get_func_path(func, language):
    return os.path.join(data_path_dict[language], func)

def predict_function(path, language):
    return  func_model[language].predict(path)

def creat_file(file_path, source_text):
    f = open(file_path, 'w+',encoding='UTF-8')
    f.write(source_text)


if __name__ == "__main__":
    data_path = '../../data/leetcode/raw'
    ret = clc.load_data(data_path, "java")
    ret = recommend_code("sdjklalasdjfsdf")
    print(ret)
