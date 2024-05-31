import time
import datetime
import threading
import notion_DB_call
import function


def sync_notion_data():
    """노션 API를 호출하여 데이터베이스를 동기화하고 데이터 프레임을 반환하는 함수."""
    # 노션 API 호출해서 DB 연결
    nc = notion_DB_call.notion_API()

    # 조회할 노션 key 리스트, key가 있다고 다 되는건 아니고 노션에서 연계등록 해야함.
    all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
               "49e1a704e0ae41679775e9f1194d9068", "e3230b6283354a798dfe0636f5e340a1", "63724ababa844d25811a503019b157ba"]  # [제품 현황 관리, 계약관리, 기타서류, 업무]

    # 노션 DB 데이터 추출
    notion_data = nc.notion_readDatabase(all_key)

    # 노션 데이터를 row_name, Properties, URL 추출해서 저장
    notion_data_result = function.extract_properties_to_array(notion_data)

    # [제품 현황 관리, 계약관리, 기타서류] 각 변수 할당
    product_manage = function.make_dataframe(notion_data_result[0])
    contract_manage = function.make_dataframe(notion_data_result[1])
    etc_manage = function.make_dataframe(notion_data_result[2])
    Task = function.make_dataframe(notion_data_result[3])

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

    # 데이터 프레임 숫자를 금액 단위로, 일반 숫자 텍스트로 변환하는 부분
    # 금액 단위로 변환되는 열 목록
    currency_columns = ["계약단가", "라이선스 총액", "계약총액"]
    # 숫자 텍스트로 변환되는 열 목록
    number_columns = ["라이선스 수", "계약잔여일"]

    # 각 데이터 프레임을 처리하여 열들을 변환
    product_manage = function.process_dataframe(
        product_manage, currency_columns, number_columns)
    contract_manage = function.process_dataframe(
        contract_manage, currency_columns, number_columns)
    etc_manage = function.process_dataframe(
        etc_manage, currency_columns, number_columns)

    Task = function.process_dataframe(
        Task, currency_columns, number_columns)

    return product_manage, contract_manage, etc_manage, Task


def run_at_specific_times():
    """특정 시간에 sync_notion_data 함수를 실행하는 함수."""
    while True:
        current_time = datetime.datetime.now().time()
        # 실행 시간 설정 (오전 7시, 오후 12시)
        if current_time.hour == 7 and current_time.minute == 0 or current_time.hour == 12 and current_time.minute == 0:
            sync_notion_data()
            # 스크립트가 실행된 후 60초 동안 대기하여 같은 시간에 여러 번 실행되지 않도록 함
            time.sleep(60)
        # 1분마다 현재 시간을 확인
        time.sleep(60)


def start_sync_in_background():
    """동기화 작업을 백그라운드에서 시작하는 함수."""
    sync_thread = threading.Thread(target=run_at_specific_times, daemon=True)
    sync_thread.start()


# 모듈이 임포트될 때 최초 한 번 실행
product_manage, contract_manage, etc_manage, Task = sync_notion_data()

# 동기화 작업을 백그라운드에서 시작
start_sync_in_background()
