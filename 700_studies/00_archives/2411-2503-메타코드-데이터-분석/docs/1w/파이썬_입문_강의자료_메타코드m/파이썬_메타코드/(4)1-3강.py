# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 11:02:46 2021

@author: 임영화이준배
"""

# =============================================================================
# 조건문
# 조건이 참이냐 거짓이냐에 따른 로직 구성
# if: 조건이 참이면 if 문 안의 로직
# elif: if 조건이 틀리고 현재 조건이 많으면
# else: if/elif 조건이 다 틀렸을 때
# =============================================================================

score = 30

if score < 30:
    print("fail")

elif score >= 30:
    print("pass")
    
else :
    print("error")
    
    
#if와 elif를 같이 쓰는 경우는 두 조건이 달라야 하며, 연속되게 조건을 비교하는 경우이다.
    
score = 90    
if score > 60:
    print("pass")
    
elif score>80:
    print("great")

# 두 조건이 중복되지만 둘다 실행되게 하려면 if문을 독립적으로 사용해야 한다.
score = 90    
if score > 60:
    print("pass")
    
if score > 80:
    print("Summa Cum")
    
        
# =============================================================================
# 조건이 참이냐 거짓이냐에 따른 로직 구성 
# for 문 
# for 변수  in 리스트, 튜플, 문자열 (반복 가능한 객체):
#     무엇인가를 처리
# =============================================================================
# for loop : 정해진 횟수동안 반복해서 돌아가는 구문으로 가장 많이 쓰인다고 볼 수 있다.
for i in range(5):
    print(i)
    
for i in [0,1,2,3,4]:
    print(i)
    
for i in ['apple', 'banana', 'cheery']:
    print(i)
    
    
#조건문이 True 인 동안 while 문 안의 문장이 반복해서 실행됨
#특정 상황에서 반복을 중지하기 while 문 안에서 조건을 제어함
#구문
#while 조건문:
#    처리
i = 0
while i < 10:
    print(i)
    i+=1
    
    
# =============================================================================
# break 
# 반복문 안에서 특정 조건이 되어 반복문을 빠져 나올 때 사용
# for 문에도 똑같이 적용 가능
# continue
# 반복문을 중단시키지 않고 다음 반복으로 넘어갈 때 사용
# 
# =============================================================================

# break과 continue는 for loop에도 그대로 사용할 수 있으며 나중에 배우는
#    pandas DataFrame 등에서도 상당히 많이 사용된다.

while True: # 구문 내에서 break이 되지 않으면 계속 반복된다.
    input_data = input("정수의 짝/홀을 알려드립니다. \n 종료하시려면 . 입력\n")
    if not input_data.isnumeric() :
        break
        
    elif int(input_data) % 2 == 0 :
        print("{}는 짝수입니다".format(input_data))
    elif int(input_data) % 2 == 1 :
        print("{}는 홀수입니다".format(input_data))
    
   

# 조건문은 맨 위에서부터 순서대로 확인된다.
while True: # 구문 내에서 break이 되지 않으면 계속 반복된다.
    input_data = input("정수의 짝/홀을 알려드립니다. \n 종료하시려면 . 입력\n")

    if int(input_data) % 2 == 0 :
        print("{}는 짝수입니다".format(input_data))
    elif int(input_data) % 2 == 1 :
        print("{}는 홀수입니다".format(input_data))
    elif not input_data.isnumeric() :
    
        break
    
    
#리스트와 반복문
name = ['이정재', '박해수', '오영수', '위하준', '정호연', '허성태', '미주령']
for i in name:
    print(i)
    
#인덱스의 위치도 알려주는 enumerate()
for i, j in enumerate(name):
    print(i,j)
    
    
#리스트에서는 리스트 속 데이터에서 조건에 맞는 데이터를 가져오는 다른 방법이 있다.
# 약속된 구문으로 숙지해두자.
lst = list(range(9))
lst_odd = [x for x in lst if x % 2 ==1]
lst_even = [x for x in lst if x % 2 ==0]


#아래와 같이 for문과 if문을 사용할수도 있지만 위에 구문이 편하다.
new_lst_odd=[]
new_lst_even=[]
for i in range(9):
    if lst[i]%2 == 1:
        new_lst_odd.append(lst[i])
    else:
        new_lst_even.append(lst[i])
        
        
        
        
# <<<<과제>>>>    
#아래 list를 a라는 dictionary에 1번 : 이정재, 2번: 박해수 식으로 딕셔너리를 만들어보자
name = ['이정재', '박해수', '오영수', '위하준', '정호연', '허성태', '미주령']
        
        














# 첫번째 방법        
a = dict()
b = []
for i in range(1,len(name)+1):
   b.append("{}번".format(i))
   
   
for i in range(0,len(name)):
    a[b[i]] = name[i]



    
        
        
# 두번째 방법        
a = dict(zip(b,name))
