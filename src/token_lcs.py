import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from src import code_language_classifier as clc
from src.text_based_similarities import Levenshtein_distance

data_path = "../data/leetcode/raw"


def init_tokenizer():
    java_data = clc.load_data(data_path, "java")
    tokenizer = Tokenizer(filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',)
    tokenizer.fit_on_texts(java_data)
    # save
    f = open('tokenizer_lcs.pkl', 'wb')
    pickle.dump(tokenizer, f)
    f.close()


def code2text(path):
    text = open(path, encoding='UTF-8').read()
    return text


def token_lcs(text1, text2):
    f1 = open('tokenizer_lcs.pkl', 'rb')
    tokenizer = pickle.load(f1)
    f1.close()
    seq1 = tokenizer.texts_to_sequences([text1])[0]
    seq2 = tokenizer.texts_to_sequences([text2])[0]
    return Levenshtein_distance.Levenshtein_similarity(seq1, seq2)


if __name__ == "__main__":
    init_tokenizer()
    text1 = code2text("../data/leetcode/raw/solutions/_1.java")
    text2 = code2text("../data/leetcode/raw/solutions/_2.java")
    similarity = token_lcs(text1, text2)
    print(similarity)