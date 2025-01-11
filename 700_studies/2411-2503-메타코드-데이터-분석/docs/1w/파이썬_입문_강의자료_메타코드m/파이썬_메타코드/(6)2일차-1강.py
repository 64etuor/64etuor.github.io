# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 21:07:13 2021

@author: 3600
"""


f = open('test.txt','r',encoding='utf8')
line = f.readlines()
f.close()


f = open('정보.txt','r',encoding='utf8')
line = f.readlines()
f.close()

print(line) 
# 받아온 결과의 \n를 없애본다.
#결과  ['이름:이상훈', '지역:서울', '나이:32', '성별:남']


















result = []
for i in line:
    temp = i.replace("\n","")
    result.append(temp)


# list의 각 원소의 : 로 구분해보자
# 결과 [['이름', '이상훈'], ['지역', '서울'], ['나이', '32'], ['성별', '남']]
















result2 = []    
for i in range(len(line)):
    temp = result[i].split(":")
    result2.append(temp)












#각각의 string으로 분리해본다
# 결과 ['이름', '이상훈', '지역', '서울', '나이', '32', '성별', '남']












flat_list = [item for sublist in result2 for item in sublist]
