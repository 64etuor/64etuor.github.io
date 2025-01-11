# -*- coding: utf-8 -*-
# =============================================================================
# 내용
# 앞에서 배운 txt 읽어오는 법을 사용하여 txt파일을 읽어오고
# 내용에 있는 자료들을 , 로 구분한다.
# txt에 있는 자료들은 코인가격이라고 생각한다.
# txt에서 읽어오면 list로 받아와지며 그 안의 데이터는 string이다.
# 빈칸이 포함되어 있으며, list의 요소인 string들을 float으로 변경해본다.
# 
# 변경하는 과정은 각 요소들을 for문을 사용해서 변경해본다
# 변경하는 과정에서 빈칸때문에 오류가 발생할 수 있는데 이때 try except 구문을 사용한다.
# =============================================================================

f = open('coin.txt','r',encoding='utf8')
line = f.readlines()
f.close()

#콤마를 구분으로 쪼갠다   
result = line[0].split(",")
#리스트 안의 string을 float으로 바꿔주는 방법1
result = list(map(float,result))
#리스트 안의 string을 float으로 바꿔주는 방법2    
result = [float(x) for x in result]
#위 두가지 모두 "" 빈칸 때문에 작동이 안된다.

#for문을 사용해 하나씩 바꿔본다.
for i in range(len(result)):
    result[i] = float(result[i])
    print(i,result[i],type(result[i])) # 여기도 빈칸에서 막힌다.
    
#try & except 
for i in range(len(result)):
    try:
        result[i] = float(result[i])
        print(i,result[i],type(result[i])) # 여기도 빈칸에서 막힌다.
    except:
        print("리스트 {}번째에서 error 발생, 다음으로 넘어갑니다".format(i))
  
   
    
print(result)



result = [8,9,10,"",11,12,"",13]

# 각 원소들의 타입은 ?
for i in result:
    print(type(i))


# pass, continue, raise error

for i in result:
    if i > 10:
        print(i)

#Try & except
for i in result:
    try:
        if i > 10:
            print(i)
    except:
        print("대소비교불가")
        
        
for i in result:
    try:
        if i > 10:
            if i == 11:
                print("11발견")
                pass # break은 ?
            print(i) # 핵심
    except:
        print("대소비교불가")
        continue



for i in result:
    try:
        if i > 10:
            if i == 11:
                print("11발견")
                continue
            print(i) # 핵심
    except:
        print("대소비교불가")
        
        
for i in result:
    try:
        if i > 10:
            if i == 11:
                print("11발견")
                raise Exception("에러")
            print(i) # 핵심
    except Exception as e:
        print(e)
        # print("대소비교불가")



for i in result:
    try:
        if i > 10:
            print(i)
        pass
    except Exception as e:
        print(e)
        # print("대소비교불가")
        
        
        
        
        
# 과제
# 예외처리 구문에서 pass와 continue의 차이점을 서술하시오
        
        
        
        
        
        
        
        
        
        
# 답안 : pass는 남은 코드를 실행하지만, continue는 다음 loop로 넘어간다
        
        