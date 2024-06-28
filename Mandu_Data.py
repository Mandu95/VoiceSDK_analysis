import notion_DB_call
import datetime
import Mandu_Function as Mandu_F
import Mandu_DA as Mandu_D


def Notion_Data_Readysetting():
    """노션 API를 호출하여 데이터베이스를 동기화하고 데이터 프레임을 반환하는 함수."""
    print(f"[{datetime.datetime.now()}] 시작: 노션 데이터 동기화")

    # 노션 API 호출해서 DB 연결
    nc = notion_DB_call.notion_API()

    # 조회할 노션 key 리스트, key가 있다고 다 되는건 아니고 노션에서 연계등록 해야함.
    all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
               "49e1a704e0ae41679775e9f1194d9068", "e3230b6283354a798dfe0636f5e340a1", "63724ababa844d25811a503019b157ba", "3e84536d6c2548488cb5f9d4c4ed9ef3"]  # [제품 현황 관리, 계약관리, 기타서류, 업무, 담당자]

    # 노션 DB 데이터 추출
    notion_data = nc.notion_readDatabase(all_key)
    print(f"[{datetime.datetime.now()}] 노션 데이터베이스에서 데이터 추출 완료")

    # 노션 데이터를 row_name, Properties, URL 추출해서 저장
    notion_data_result_list = Mandu_F.Notion_properties_URL(notion_data)
    print(f"[{datetime.datetime.now()}] 데이터 속성 추출 완료")

    # [제품 현황 관리, 계약관리, 기타서류] 데이터프레임 생성
    cop_manage_df = Mandu_F.make_dataframe(notion_data_result_list[0])
    contract_manage_df = Mandu_F.make_dataframe(notion_data_result_list[1])
    etc_manage_df = Mandu_F.make_dataframe(notion_data_result_list[2])
    Task_df = Mandu_F.make_dataframe(notion_data_result_list[3])
    customer_df = Mandu_F.make_dataframe(notion_data_result_list[4])
    print(f"[{datetime.datetime.now()}] 데이터프레임 생성 완료")

    # [제품 현황 관리, 계약관리, 기타서류] 관계형 데이터 텍스트로 기입
    cop_manage_df = Mandu_F.change_relation_data(
        cop_manage_df, notion_data[2], "기타문서 (견적서, NDA 등)", "문서이름")
    cop_manage_df = Mandu_F.change_relation_data(
        cop_manage_df, notion_data[4], "담당자", "고객 컨택 담당자")
    cop_manage_df = Mandu_F.change_relation_data(
        cop_manage_df, notion_data[2], "📦 업무 일정", "업무")
    cop_manage_df = Mandu_F.change_relation_data(
        cop_manage_df, notion_data[1], "계약관리", "계약명")
    contract_manage_df = Mandu_F.change_relation_data(
        contract_manage_df, notion_data[0], "제품 현황 관리", "업체 이름")
    etc_manage_df = Mandu_F.change_relation_data(
        etc_manage_df, notion_data[0], "발송 대상", "업체 이름")
    Task_df = Mandu_F.change_relation_data(
        Task_df, notion_data[0], "프로젝트 (제품)", "업체 이름")
    customer_df = Mandu_F.change_relation_data(
        customer_df, notion_data[0], "프로젝트", "업체 이름")

    # 리스트를 문자열로 변환
    cop_manage_df = Mandu_F.normalize_column_lists(cop_manage_df)
    contract_manage_df = Mandu_F.normalize_column_lists(contract_manage_df)
    etc_manage_df = Mandu_F.normalize_column_lists(etc_manage_df)
    Task_df = Mandu_F.normalize_column_lists(Task_df)
    customer_df = Mandu_F.normalize_column_lists(customer_df)

    # 날짜, 금액 단위 알맞게 변환
    cop_manage_df = Mandu_F.Change_data(
        cop_manage_df, ["생성 일시", "정보 최신화 날짜", "계약시작일", "계약종료일"])
    print(f"[{datetime.datetime.now(), len(cop_manage_df)}] 업체 현황 데이터 준비 완료")
    contract_manage_df = Mandu_F.Change_data(contract_manage_df, "계약시작일")
    print(f"[{datetime.datetime.now(), len(contract_manage_df)}] 계약서 데이터 준비 완료")
    etc_manage_df = Mandu_F.Change_data(etc_manage_df)
    print(f"[{datetime.datetime.now(), len(etc_manage_df)}] 기타서류 데이터 준비 완료")
    Task_df = Mandu_F.Change_data(Task_df, "업무기간")
    print(f"[{datetime.datetime.now(), len(Task_df)}] 업무 데이터 준비 완료")
    customer_df = Mandu_F.Change_data(customer_df, "최초 컨택 날짜")
    print(f"[{datetime.datetime.now(), len(customer_df)}] 고객 데이터 준비 완료")
    return cop_manage_df, contract_manage_df, etc_manage_df, Task_df, customer_df


def main(df=None, action_name=None):

    # 데이터를 활용한 분석 행위가 아닐 때 (초기 데이터 세팅)
    if action_name is None:
        cop_manage_df, contract_manage_df, etc_manage_df, Task_df, customer_df = Notion_Data_Readysetting()
        return cop_manage_df, contract_manage_df, etc_manage_df, Task_df, customer_df

    # 데이터를 활용한 분석
    else:
        print(action_name, "분석을 시작합니다.")
        action_name = [action_name] if not isinstance(
            action_name, list) else action_name
        for A in action_name:
            if A == "내용 업데이트 업체":
                DF_update_one_Week_cop = Mandu_D.update_one_week_cop(df)
                print(A, "데이터 준비 완료")
                return DF_update_one_Week_cop
            elif A == "신규 업체":
                DF_New_cop = Mandu_D.new_cop_data(df, "생성 일시")
                print(A, "데이터 준비 완료")
                return DF_New_cop

            elif A == "매입/매출 데이터":

                Data_all, Data_buy, Data_sell, Data_no_info = Mandu_D.View_contract_status(
                    df)
                print(A, "데이터 준비 완료")
                return Data_all, Data_buy, Data_sell, Data_no_info

            elif A == "계약전환률":

                contract_df_Demo, demo_to_contract_df = Mandu_D.DA_cop_convert_to_contract(
                    df)
                print(A, "데이터 준비 완료")
                return contract_df_Demo, demo_to_contract_df

            elif A == "월별 매출성과":

                this_month_df, df_last_3_months, df_last_6_months = Mandu_D.moeny_sum_month(
                    df)
                print(A, "데이터 준비 완료")
                return this_month_df, df_last_3_months, df_last_6_months

            elif A == "분기별 매출성과":

                quarter_1_df, quarter_2_df, quarter_3_df, quarter_4_df = Mandu_D.moeny_quater(
                    df)
                print(A, "데이터 준비 완료")
                return quarter_1_df, quarter_2_df, quarter_3_df, quarter_4_df
