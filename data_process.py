import notion_DB_call
import mandu_function
import pandas as pd

# notion api 호출해서 DB 연결
nc = notion_DB_call.notion_API()

# 조회할 DB 키 리스트
all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
           "49e1a704e0ae41679775e9f1194d9068"]

# DB 데이터 추출
data = nc.notion_readDatabase(all_key)

# 첫 번째 DB에서 properties 속성만 추출
data1 = data[0]['properties']
print(data[0]['properties'][60]['계약구분']['rollup']['array'])

# URL 데이터를 DataFrame으로 변환
url_data = data[0]['url']
url_df = url_data.to_frame(name='URL')
print(url_df)

# 표 View를 위한 속성 추출
row_name = mandu_function.df_col(data1)

# 값 추출
df = mandu_function.extract_data(data1, row_name)

# 두 번째 DB의 데이터 사용
data2 = data[1]
df = mandu_function.change_contract_data(data2, df)

print(df.head())