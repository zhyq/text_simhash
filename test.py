#!/usr/bin/env python
# -*- coding: utf-8 -*-
from similarity import *
sy = similarity('similarity.cfg')

def test():
    #种子做成 simhash库
    str = "我是南翔技工拖拉机学院手扶拖拉机专业的。不用多久，我就会升职加薪，当上总经理，出任CEO，走上人生巅峰。,清华大"
    m = sy.extract_keywords(str)
    for (k,v) in m:
        print k,v
    hash_model,doc_dict = sy.simhash_bucket()
    str = u"我爱打球"
    sh1 = sy.text_genhash(str)
    print sy.find_similarity(sh1,hash_model)
    #save_model(hash_model, model_path)
    #save_model(doc_dict, doc_dict_path)
    
    
    #预测文章
    
if __name__ == '__main__':
    num = 10
    while(num):
        test()
        num--
