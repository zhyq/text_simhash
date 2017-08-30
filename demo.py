#!/usr/bin/env python
# -*- coding: utf-8 -*-

# step 1 import
from similarity import *
# setp 2 init (includeing config file )
sy = similarity('similarity.cfg')

def test():
    str = "我是南翔技工拖拉机学院手扶拖拉机专业的。不用多久，我就会升职加薪，当上总经理，出任CEO，走上人生巅峰。,清华大"
    # step 3 call generate simhash code
    sh = sy.text_genhash(str)
    print sh



if __name__ == '__main__':
    num = 10
    while(num):
        test()
        num=num-1
