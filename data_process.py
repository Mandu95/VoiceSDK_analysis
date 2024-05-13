import notion_DB_call

nc = notion_DB_call.notion_API()  ##notion api 호출해서 DB 연결
all_key = ["8f0bbf0eae504cd29a45080803aa74cf", "2301ef1117d14da1a495e36a65fb1e74"] ##내가 조회하고자 하는 DB 키 정적입력 type = list
data = nc.notion_readDatabase(all_key)  ## DB 데이터 추출
database_properties = nc.extract_properties(data) ## dic 형태에서 properties 속성 값만 추출

