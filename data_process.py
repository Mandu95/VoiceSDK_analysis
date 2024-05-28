import notion_DB_call
import mandu_function
import pandas as pd

# notion api 호출해서 DB 연결
nc = notion_DB_call.notion_API()

# 조회할 DB 키 리스트
all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
           "49e1a704e0ae41679775e9f1194d9068", "e3230b6283354a798dfe0636f5e340a1"]  # [제품 현황 관리, 계약관리, 기타서류]

# DB 데이터 추출
data = nc.notion_readDatabase(all_key)

# 첫 번째 DB에서 properties 속성만 추출
product_management = data[0]['properties']
print(data[0]['properties'][60]['계약구분']['rollup']['array'])

# URL 데이터를 DataFrame으로 변환
url_data = data[0]['url']
url_df = url_data.to_frame(name='URL')

# 표 View를 위한 속성 추출
row_name = mandu_function.df_col(product_management)

# 값 추출
product_management = mandu_function.extract_data(product_management, row_name)

# 두 번째 DB의 데이터 사용
contract_management_db = data[1]
product_management = mandu_function.change_contract_data(
    contract_management_db, product_management)

etc_document_db = data[2]

product_management = mandu_function.change_etc_docu_data(
    etc_document_db, product_management)

###############################################################################################

# 기타서류 DB에서 properties 속성만 추출
etc_document = data[2]['properties']

# 표 View를 위한 속성 추출
etc_document_row_name = mandu_function.df_col(etc_document)
# 값 추출
etc_document = mandu_function.extract_data(etc_document, etc_document_row_name)
# 두 번째 DB의 데이터 사용
product_management_db = data[0]
etc_document = mandu_function.change_company_name_data(
    product_management_db, etc_document)


###############################################################################################
# 계약서 관리 DB 데이터 활용
contract_management = data[1]['properties']
# 계약서 관리 DB View를 위한 속성 추출
contract_management_row_name = mandu_function.df_col(contract_management)

# 값 추출
contract_management = mandu_function.extract_data(
    contract_management, contract_management_row_name)

print(contract_management.loc[0])
# 제품 현황 관리 DB에서 데이터 값 비교하고 변환
product_management_db = data[0]

contract_management = mandu_function.change_data_type(
    product_management_db, contract_management)
