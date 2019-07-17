#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging
import os
import time
from multiprocessing import cpu_count
import tinysegmenter
import re
import wget
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 这里手动设置下
VECTORS_SIZE = 50
JA_WIKI_TEXT_FILENAME = 'jawiki-latest-text.txt'
JA_WIKI_SENTENCES_FILENAME = 'jawiki-latest-text-sentences.txt'

JA_WIKI_TEXT_TOKENS_FILENAME_DIR = 'split'
JA_WIKI_SENTENCES_TOKENS_FILENAME = 'jawiki-latest-text-sentences-tokens.txt'

JA_VECTORS_MODEL_FILENAME = 'ja-gensim.{}d.data.model'.format(VECTORS_SIZE)
JA_VECTORS_TEXT_FILENAME = 'ja-gensim.{}d.data.txt'.format(VECTORS_SIZE)


def generate_vectors(input_filename, output_filename, output_filename_2):

    if os.path.isfile(output_filename):
        model = Word2Vec.load('ja-gensim.50d.data.model')
    else:
        model = None

    start = time.time()
    for file in os.listdir(input_filename):
        logging.info('We are processing '+file)
        if not model:
            model = Word2Vec(LineSentence(JA_WIKI_TEXT_TOKENS_FILENAME_DIR+'/'+file),
                             size=VECTORS_SIZE,
                             window=5,
                             min_count=5,
                             workers=4,
                             iter=5)
        else:
            model.build_vocab(LineSentence(JA_WIKI_TEXT_TOKENS_FILENAME_DIR+'/'+file), update=True)
            model.train(LineSentence(JA_WIKI_TEXT_TOKENS_FILENAME_DIR+'/'+file), total_examples=model.corpus_count, epochs=model.iter)

        model.save(output_filename)
        model.wv.save_word2vec_format(output_filename_2, binary=False)
        logging.info(file + ' has been finished')
    logging.info('Finished generate_vectors(). It took {0:.2f} s to execute.'.format(round(time.time() - start, 2)))


if __name__ == '__main__':
    generate_vectors(JA_WIKI_TEXT_TOKENS_FILENAME_DIR, JA_VECTORS_MODEL_FILENAME, JA_VECTORS_TEXT_FILENAME)