import notion_DB_call
import function
import datetime


## Notion에서 데이터 로딩하는 함수 ##
def First_data_setting():
    """노션 API를 호출하여 데이터베이스를 동기화하고 데이터 프레임을 반환하는 함수."""
    print(f"[{datetime.datetime.now()}] 시작: 노션 데이터 동기화")

    # 노션 API 호출해서 DB 연결
    nc = notion_DB_call.notion_API()

    # 조회할 노션 key 리스트, key가 있다고 다 되는건 아니고 노션에서 연계등록 해야함.
    all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
               "49e1a704e0ae41679775e9f1194d9068", "e3230b6283354a798dfe0636f5e340a1", "63724ababa844d25811a503019b157ba"]  # [제품 현황 관리, 계약관리, 기타서류, 업무]

    # 노션 DB 데이터 추출
    notion_data = nc.notion_readDatabase(all_key)
    print(f"[{datetime.datetime.now()}] 노션 데이터베이스에서 데이터 추출 완료")

    # 노션 데이터를 row_name, Properties, URL 추출해서 저장
    notion_data_result = function.extract_properties_to_array(notion_data)
    print(f"[{datetime.datetime.now()}] 데이터 속성 추출 완료")

    # [제품 현황 관리, 계약관리, 기타서류] 데이터프레임 생성
    product_manage = function.make_dataframe(notion_data_result[0])
    contract_manage = function.make_dataframe(notion_data_result[1])
    etc_manage = function.make_dataframe(notion_data_result[2])
    Task = function.make_dataframe(notion_data_result[3])
    print(f"[{datetime.datetime.now()}] 데이터프레임 생성 완료")

    # [제품 현황 관리, 계약관리, 기타서류] 관계형 데이터 텍스트로 기입
    product_manage = function.change_relation_data(
        product_manage, notion_data[2], "기타문서 (견적서, NDA 등)", "문서이름")
    product_manage = function.change_relation_data(
        product_manage, notion_data[2], "📦 업무 일정", "업무")
    product_manage = function.change_relation_data(
        product_manage, notion_data[1], "계약관리", "계약명")
    contract_manage = function.change_relation_data(
        contract_manage, notion_data[0], "제품 현황 관리", "업체 이름")
    etc_manage = function.change_relation_data(
        etc_manage, notion_data[0], "발송 대상", "업체 이름")
    Task = function.change_relation_data(
        Task, notion_data[0], "분류", "업체 이름")

    return product_manage, contract_manage, etc_manage, Task

## 로딩 된 데이터프레임 일부 데이터 형태를 변환 ##


def Change_data(df, column_name=None):

    df = function.Change_date_iso8601(df, column_name)
    df = function.Change_data_type(df)

    return df


product_manage, contract_manage, etc_manage, Task = First_data_setting()

product_manage = Change_data(product_manage, ["생성 일시", "정보 최신화 날짜"])
print(f"[{datetime.datetime.now(), len(product_manage)}] 업체 현황 데이터 준비 완료")
contract_manage = Change_data(contract_manage)
print(f"[{datetime.datetime.now(), len(contract_manage)}] 계약서 데이터 준비 완료")
etc_manage = Change_data(etc_manage)
print(f"[{datetime.datetime.now(), len(etc_manage)}] 기타서류 데이터 준비 완료")
Task = Change_data(Task, "업무기간")
print(f"[{datetime.datetime.now(), len(etc_manage)}] 업무 데이터 준비 완료")
