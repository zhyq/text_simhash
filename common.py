#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import jieba
import jieba.analyse
import cPickle


from text_cleaner import remove, keep
from text_cleaner.processor.misc import (
    URL,
    RESTRICT_URL,
    ESCAPED_WHITESPACE,
    WECHAT_EMOJI,
)
from text_cleaner.processor.processor import (
    RegexProcessor,
)

from text_cleaner.processor.common import (
    ALPHA,
    DIGIT,
)

from text_cleaner.processor.chinese import (
    CHINESE_CHARACTER,
    CHINESE,
    CHINESE_SYMBOLS_AND_PUNCTUATION,
)
class cn:
    def __init__(self,dict_file = None, idf_path = None, stopwords_path = None):
        self.cn(dict_file, idf_path, stopwords_path)
    def cn(self, dict_file = None, idf_path = None, stopwords_path = None):
        if dict_file is not None:
            jieba.set_dictionary(dict_file)
            #jieba.load_userdict(dict_file)
        if idf_path is not None:
            jieba.analyse.set_tfidf_words(idf_path)
        if stopwords_path is not None:
            jieba.analyse.set_stop_words(stopwords_path)
            
    def clean(self, text):
        keep_list = []
        #rm_list = [URL, ESCAPED_WHITESPACE,WECHAT_EMOJI ]
        rm_list = [RESTRICT_URL, ESCAPED_WHITESPACE, WECHAT_EMOJI ]

        keep_list.append(CHINESE_CHARACTER)
        keep_list.append(ALPHA)
        keep_list.append(DIGIT)

        text = remove(
            text,
            rm_list,
        )
    
        text = keep(
            text,
            keep_list,
        )

        return text.strip()

    def wash(self, text):
        # 1. html to text
        text = re.sub(r'</?\w+[^>]*>','',text)
        
        # 2. tolower()
        text = text.lower()

        # 3. text_cleaner
        tokens = self.clean(text)

        text = "".join(tokens).replace(' ', '')

        return text
    
    def segment(self, content):
        ''' segment '''
        result = ''
        stop_words = None
        feature_words = None
        words = jieba.cut(content,HMM=False)
        if stop_words is not None:
            words = filter(lambda arg: arg not in stop_words,words)
        if feature_words is not None:
            words = filter(lambda arg:  arg in feature_words,words)

        result = " ".join(words)
        return result.strip()

    def extract_keywords(self, content, topK):
        keyWord = jieba.analyse.extract_tags(
            #content, topK, withWeight=True, allowPOS=('n','a','v','b','ns','nr','nt','nz','ng','vn','vg','vd','an','ag'))
            content, topK, withWeight=True, allowPOS=())
        return keyWord

        
    def save_model(self,item,path):
        cPickle.dump(item, open(path, "wb"))

    def load_model(self,path):
        model = cPickle.load(open(path, "rb"))
        return model
        
    def read_list(self, input_filepath):
        doclist = []
        f_in = open(input_filepath)
        while True:
            line = f_in.readline().strip().decode('utf8')
            if not line:
                break
            try:
                doclist.append(line)
            except:
                pass
        f_in.close()
        return doclist
