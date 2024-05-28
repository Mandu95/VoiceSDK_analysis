import notion_DB_call
import function


# notion api 호출해서 DB 연결
nc = notion_DB_call.notion_API()

# 조회할 notion key list, key가 있다고 다 되는건 아니고 notion에서 연계등록 해야함.
all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
           "49e1a704e0ae41679775e9f1194d9068", "e3230b6283354a798dfe0636f5e340a1"]  # [제품 현황 관리, 계약관리, 기타서류]

# notion DB 데이터 추출
notion_data = nc.notion_readDatabase(all_key)


# notion data를 row_name, Properites, URL 추출해서 저장
notion_data_result = function.extract_properties_to_array(notion_data)

temp = notion_data[1]
print(temp['id'])
print(temp['properties'][0]["계약명"]['title'][0]['plain_text'])


# [제품 현황 관리, 계약관리, 기타서류] 각 변수 할당
product_manage = function.make_dataframe(notion_data_result[0])
contract_manage = function.make_dataframe(notion_data_result[1])
etc_manage = function.make_dataframe(notion_data_result[2])


# [제품 현황 관리, 계약관리, 기타서류] 관계형 데이터 텍스트로 기입
product_manage = function.change_relation_data(
    product_manage, notion_data[2], "기타문서 (견적서, NDA 등)", "문서이름")
product_manage = function.change_relation_data(
    product_manage, notion_data[1], "계약관리", "계약명")
contract_manage = function.change_relation_data(
    contract_manage, notion_data[0], "제품 현황 관리", "업체 이름")
etc_manage = function.change_relation_data(
    etc_manage, notion_data[0], "발송 대상", "업체 이름")
