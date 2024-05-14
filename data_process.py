import notion_DB_call
import mandu_function

nc = notion_DB_call.notion_API()  ##notion api 호출해서 DB 연결
all_key = ["69aeff6ca32d4466ad4748dde3939e8b"] ##내가 조회하고자 하는 DB 키 정적입력 type = list
data = nc.notion_readDatabase(all_key)  ## DB 데이터 추출
database_properties = nc.extract_properties(data) ## dic 형태에서 properties 속성 값만 추출


count = len(database_properties[0])
status_fliter = []
for A in range(count):
    
    try:
        if database_properties[0][A]['상태']['status']['name'] is not None:
            status_fliter.append(database_properties[0][A]['상태']['status']['name'])
            
    except Exception as e:
        print("Database를 다시 확인하시오, 데이터가 비어서 그럴거에요!")

status_fliter = mandu_function.find_same_data(status_fliter)    

goods_fliter = []
for B in range(count):
    
    try:
        
        if database_properties[0][B]['연관 제품']['select']['name'] is not None :

            goods_fliter.append(database_properties[0][B]['연관 제품']['select']['name'])
            
    except Exception as e:
        print("Database를 다시 확인하시오, 데이터가 비어서 그럴거에요!")
        
goods_fliter = mandu_function.find_same_data(goods_fliter)
print(goods_fliter)


