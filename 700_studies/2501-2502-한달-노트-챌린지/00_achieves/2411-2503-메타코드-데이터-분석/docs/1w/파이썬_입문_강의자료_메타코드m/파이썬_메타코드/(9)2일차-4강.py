# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 17:48:35 2021

@author: 3600
"""
# =============================================================================
# Pandas 라이브러리
# 시리즈 : 한줄짜리.
# =============================================================================
import pandas as pd
example = pd.Series() # 시리즈의  S는 대문자여야함.

# 시리즈를 만드는법 1. 리스트를 활용
lst = [1,2,3,4,5]
ex_1 = pd.Series(lst)
print(ex_1,type(ex_1))

# 시리즈의 loc, iloc 인덱싱
ex_1.loc[0]
ex_1.iloc[0]

dictionary = {"성별":"남자","이름":"이상훈","지역":"서울","나이":"32"}
ex_2 = pd.Series(dictionary)
print(ex_2)

ex_2.loc[1]
ex_2.iloc[1]
ex_2.loc['이름']

#딕셔너리 형태를 시리즈로 만들면 Key가 인덱스로 지정된다
#인덱스로 지정된 딕셔너리의 key를 데이터로 빼내는 방법은 reset_index() 함수이다.
ex_2.reset_index(drop = True) # drop=True를 하면 아에 인덱스가 사라진다
ex_2.reset_index(drop = False) # drop=False를 하면 인덱스가 데이터 안으로 들어간다
ex_2.reset_index() #drop = FAlse는 default 값으로 생략해도 된다.
#위 코드는 ex_2에 적용되는것이 아니므로 저장을 따로 해주어야 한다.
ex_3 = ex_2.reset_index() # 열이 2개가 되면서 시리즈가 아닌 DataFrame이 되었다.
 
print(ex_3)
ex_3.loc[3,0]
ex_3.loc[3,'index']
ex_3.iloc[3,0]
ex_3.iloc[3,1]

ex_3.shape
type(ex_3)

lst_4 = [[1,2,3,4,5],[1,2,3,4,5]]
ex_4 = pd.Series(lst_4)


# =============================================================================
# 데이터프레임
# 가장 많이 사용하는 함수
# =============================================================================
import numpy as np
import pandas as pd
#array -> DataFrame
array = np.array([(3,2,31),(4,14,7)])
ex_1 = pd.DataFrame(array)


dictionary = {"성별":"남자","이름":"이상훈","지역":"서울","나이":"32"}
ex_2 = pd.DataFrame([dictionary])
ex_2 = pd.DataFrame(dictionary,index = ['1']) # 딕셔너리를 데이터프레임으로 변경시에는 key가 column이 된다.




# 0으로만 이루어진 4x4 데이터 프레임을 만드는 방법은 ??




pd.DataFrame(np.zeros((4,4)))







data = pd.read_csv("dg_csv_kospi_201912301.csv")


data.index
data.values
data.columns
data.info()
data.describe()


# 삼성전자의 정보를 모아보자
samsung = data[data['co_nm']=='삼성전자']



date = data['trd_date'].unique()
date[1]


a = data['trd_date']

first_data = data[data['trd_date']==date[1]]
second_data = first_data.sort_values(by=['market_cap','adj_prc'],ascending=[False,False])














#과제 : date 에 저장된 각 월말 마다 시가총액(market_cap) 1등부터 5등까지 기업들을 모아보시오.
#Hint1. For Loop 사용
#Hink2. 저장을 위해 save_data = pd.DataFrame()  으로 비어있는 데이터프레임을 생성
#Hink3. pd.merge()를 활용하여 dataframe을 합치는 식으로 데이터 저장
#   df1 =  pd.merge([df1,df2])

"""
(2024.11.22) 수정 안내: 
강사님께서 merge를 사용하라고 되어 있지만, 
주어진 데이터에서는 concat을 사용하는 것이 더 적합합니다. 

merge는 일반적으로 공통된 컬럼을 기준으로 데이터를 병합할 때 유용하게 사용됩니다. 
따라서 해당 부분을 concat을 활용해주시면 되겠습니다.

※ merge를 사용할 때는 두 데이터 사이의 공통된 key 값을 사용해야 합니다.
"""


















save_data = pd.DataFrame()

#답안
for i in range(len(date)):
    first_data = data[data['trd_date']==date[i]]
    second_data = first_data.sort_values(by=['market_cap'],ascending=[False])
    save_data = pd.concat([save_data,second_data.iloc[:5,:]])
