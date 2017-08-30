# -*- coding: utf-8 -*-
import numpy as np
import json

import re

class shash:
    def __init__(self):
        self.simhash=self.shash()

    def __str__(self):
        return str(self.simhash)
        
    def shash(self):
        print ''
        
    def sim_hash(self, keyword):
        keyList = []
        for (feature, weight) in keyword:
            if len(feature.strip()) <= 0:
                continue

            weight = int(weight * 100)
            #print weight, feature
            feature = self.str_hash(feature)
            temp = []
            for i in feature:
                if(i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        if(keyList==[]): #编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if(i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash


    def str_hash(self,source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]

            return str(x)



    def hamming_dis(self ,hash_l ,hash_r):
        t1 = '0b' + hash_l
        t2 = '0b' + hash_r
        n=int(t1, 2) ^ int(t2, 2)
        i=0
        while n:
            n &= (n-1)
            i+=1
        return i

    def similarity(self, hash_l,hash_r):
        a = float(hash_l)
        b = float(hash_r)
        if a > b:
            if b == 0.0:
                return a
            else:
                return a/b
        else:
            if a == 0.0:
                return b
            return b/a
            
    def simhash_bucket(self, simhashs, bucket_num):
        dic_name = []
        all = len(str(simhashs[0]))
        for i in range(bucket_num):
            dic_name.append({})
        for s in simhashs:
            bit = all / bucket_num
            num = all
            count = 0 #桶数
            while (num):
                detected_flat = 0
                num -= bit
                s_int = int('0b' + str(s), 2)
                mask = bin(s_int >> num).replace('0b', '').zfill(bit)[-bit:]  # 先取高位
                if num == 0:
                    mask_left = bin(s_int >> (num + bit)).replace('0b', '').zfill(all - num - bit)[-(all - num - bit):]
                elif num == all - bit:
                    mask_left = bin(s_int).replace('0b', '').zfill(num)[-num:]
                else:
                    mask_left = bin(s_int >> (num + bit)).replace('0b', '').zfill(all - num - bit)[
                                -(all - num - bit):] + bin(s_int).replace('0b', '').zfill(num)[-num:]
                if dic_name[count].has_key(mask):  # 查找set中的文件剩余位数是否汉明码相同。
                    dic_name[count][mask].append(mask_left)
                else:
                    dic_name[count].setdefault(mask, [mask_left])  
                    # 以64bit,分4段为例： dic_name是分的4个table。每个table，是一个索引为前16bit的simhash, 内容一个字典。字典是前16位相同时，文档内容为key,后48的simhash作为values
                count += 1
        return dic_name
        
    def find_Similarity(self,simh,dic_name,bucket_num,threadhold):
        all = len(simh)
        bit = all / bucket_num
        num = all
        count = 0
        detected_flat = 0
        while (num):

            num -= bit
            s_int = int('0b' + str(simh), 2)
            mask = bin(s_int >> num).replace('0b', '').zfill(bit)[-bit:]  # 先取高位
            if num == 0:
                mask_left = bin(s_int >> (num + bit)).replace('0b', '').zfill(all - num - bit)[-(all - num - bit):]
            elif num == all - bit:
                mask_left = bin(s_int).replace('0b', '').zfill(num)[-num:]
            else:
                mask_left = bin(s_int >> (num + bit)).replace('0b', '').zfill(all - num - bit)[
                            -(all - num - bit):] + bin(s_int).replace('0b', '').zfill(num)[-num:]
            if dic_name[count].has_key(mask):  # 查找set中的文件剩余位数是否汉明码相同。
                for hash_left in dic_name[count][mask]:
                    dist = self.hamming_dis(mask_left, hash_left)
                    if dist < threadhold or dist == threadhold:
                    # print "similar detected!"
                        return True
            count += 1
        
        return False