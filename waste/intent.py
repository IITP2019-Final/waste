#!/usr/bin/env python
# coding: utf-8
import pickle
import numpy as np
import tensorflow as tf
from konlpy.tag import Okt
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model

graph = tf.get_default_graph()


with open("data/sentences.pickle", "rb") as fr:
    sentences = pickle.load(fr)

okt = Okt()


def cleaning(sentences, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'):
    result = []

    for sent in sentences:
        processed_sent = []
        pos_tagged = okt.pos(sent)

        for token in pos_tagged:
            # if token[0].isdigit():
            # token[0] = '<NUM>'

            processed_sent.append(token[0])

        result.append(processed_sent)

    return result


cleaned_words = cleaning(sentences)


def create_tokenizer(sentences, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'):
    token = Tokenizer(filters = filters)
    token.fit_on_texts(sentences)

    return token


def max_length(sentences):
    return(len(max(sentences, key = len)))


word_tokenizer = create_tokenizer(cleaned_words)
vocab_size = len(word_tokenizer.word_index) + 1
max_length = max_length(cleaned_words)


def encoding_doc(token, sentences):
    return(token.texts_to_sequences(sentences))


encoded_doc = encoding_doc(word_tokenizer, cleaned_words)


def padding_doc(encoded_doc, max_length):
    return(pad_sequences(encoded_doc, maxlen = max_length, padding = "post"))


padded_doc = padding_doc(encoded_doc, max_length)


model = load_model("data/model.h5")


def predictions(text):
    # clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
    # test_word = word_tokenize(text)
    # test_word = [w.lower() for w in test_word]
    test_word = okt.morphs(text)
    test_ls = word_tokenizer.texts_to_sequences(test_word)

    # Check for unknown words

    if [] in test_ls:
        test_ls = list(filter(None, test_ls))

    test_ls = np.array(test_ls).reshape(1, len(test_ls))

    x = padding_doc(test_ls, max_length)



    with graph.as_default():
        pred = model.predict_proba(x)

    return pred


def get_final_output(pred, classes):
    predictions = pred[0]

    classes = np.array(classes)

    ids = np.argsort(-predictions)

    classes = classes[ids]

    predictions = -np.sort(-predictions)

    for i in range(pred.shape[1]):
        print("%s has confidence = %s" % (classes[i], (predictions[i])))
