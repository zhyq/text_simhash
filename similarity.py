#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
from common import *
from simhash import *
class similarity():
    def __init__(self, config_file = 'similarity.cfg'):
        
        ####  args ###
        cp=ConfigParser.ConfigParser()
        cp.read(config_file)

        self.dict_path = None
        self.stopword_path = None
        self.idf_path = None

        self.bucket_num = 16
        self.threadhold = 10
        self.topK = 120
        self.seed_path = "data/seed.txt"
        self.model_path = "model/hash_bucket.model"
        self.doc_dict_path = "model/doc_dict.model"

        if cp.has_option('global','bucket_num'):
            self.bucket_num = int(cp.get('global','bucket_num'))

        if cp.has_option('global','threadhold'):
            self.threadhold = int( cp.get('global','threadhold') )

        if cp.has_option('global','topK'):
            self.topK = int( cp.get('global','topK') )

        if cp.has_option('global','seed_path'):
            self.seed_path = cp.get('global','seed_path')

        if cp.has_option('global','model_path'):
            self.model_path = cp.get('global','model_path')

        if cp.has_option('global','doc_dict_path'):
            self.doc_dict_path = cp.get('global','doc_dict_path')

        if cp.has_option('global','dict_path'):
            self.dict_path = cp.get('global','dict_path')

        if cp.has_option('global','stopword_path'):
            self.stopword_path = cp.get('global','stopword_path')

        if cp.has_option('global','idf_path'):
            self.idf_path = cp.get('global','idf_path')

        self.cn = cn(self.dict_path, self.idf_path, self.stopword_path)
        self.shash = shash()
        
    def segment(self, content):
        row = content.strip().split('\t')
        wash_text = self.cn.wash(row[-1])
        seg_text = self.cn.segment(wash_text)
        row[-1] = seg_text
        return '\t'.join(row)
    
    def extract_keywords(self, content):
        return self.cn.extract_keywords(content, self.topK)

    def hamming_dis(self, simhash_l, simhash_r):
        return self.shash.hamming_dis(simhash_l, simhash_r)

    def simhash_bucket(self):
        docs = self.cn.read_list(self.seed_path)
        doc_dict = {}
        simhashs = []
        for doc in docs:
            sh = self.text_genhash(doc)
            simhashs.append(sh)
            doc_dict[sh] = doc
        hash_model = self.shash.simhash_bucket(simhashs, self.bucket_num)
        return hash_model,doc_dict
    
    def find_similarity(self, simh, dic_name):
        return self.shash.find_Similarity(simh,dic_name,self.bucket_num,self.threadhold)

    def save_model(self,item, path):
        self.cn.save_model(item, path)
    
    def load_model(self, path):
        return self.cn.load_model(path)
        
    def text_genhash(self,doc):
        """ string to simhash """
        seg = self.segment(doc)
        kw = self.extract_keywords(seg)
        return self.shash.sim_hash(kw)
