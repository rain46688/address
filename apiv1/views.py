import requests
import pandas as pd
from django.http import JsonResponse
from apiv1.models import AdmCodeList, AdmSiList, AdmDongList, AdmReeList
from django.db import IntegrityError

# 메인 로직
def main(request):
    print(" ===== main ===== ")

    # 리스트 선언
    admCodeLists= []
    admSiList=[]
    admDongList=[]
    admReeList=[]

    # 실행 로직
    try:
        print(" ===== 시도 리스트 구하기 ===== ")
        admCodeLists = address("admCodeList", AdmCodeList)

        print(" ===== 시군구 리스트 구하기 ===== ")
        admSiList = address("admSiList", AdmSiList, admCodeLists)

        print(" ===== 읍면동 리스트 구하기 ===== ")
        admDongList = address("admDongList", AdmDongList, admSiList)

        print(" ===== 리 리스트 구하기 ===== ")
        admReeList = address("admReeList", AdmReeList, admDongList)

        print(" ===== 전체 로직 완료 ===== ")

        return JsonResponse({"status" : "success"}, safe=False)
    except Exception as e:
        print(f"e : {e}")
        return JsonResponse({"status" : "fail"}, safe=False)
    
# 메인 로직 - 메인 실행안하면 디버깅 안됨
if __name__ == "__main__":
    main("main")

# 리스트 반환 로직
def address(name, db, plist=[]):
    req_data = []
    if plist == []:
        req_data = api(name, None)
    else:
        for item in plist:
            list = api(name, item.get('admCode', None))
            print(f"name : {name} / admCode : {item.get('admCode', None)}")
            if list:
                req_data.extend(list)
    print(" ===== 리스트 생성 완료 ===== ")
    savedb(req_data, db)
    print(" ===== 디비 추가 완료 ===== ")
    edata = excel(db)
    print(" ===== 엑셀 작업 완료 ===== ")
    edata.to_excel(name + ".xlsx", index=False)
    print(" ===== 리스트 반환 로직 완료 ===== ")
    return req_data

# api 호출 로직
def api(name, admCode):
        api_url = "https://api.vworld.kr/ned/data/"+name

        jsonp_params = {
            'key': '56C7879D-F177-3925-83BE-62B81A40452E',
            "domain": "http://localhost:3000/",
            "format": "json",
            "numOfRows": "1000",
            "pageNo": "1"
        }

        if admCode:
            jsonp_params["admCode"] = admCode

        response = requests.get(api_url, params=jsonp_params)

        if response.status_code == 200:
            data = data = response.json()
            # print(f"data : {data}")
            return data.get('admVOList', {}).get('admVOList', None)
        else:
            print("에러")
            return None

# pandas 저장 로직
def savedb(data, model):
    try:
        if data is not None:
            for item in data:
                # 중복된 데이터인지 확인
                existing_data = model.objects.filter(admCode=item.get('admCode', None)).first()
                if existing_data is None:
                    # 중복되지 않은 경우에만 추가
                    print(f" ===== admCode: {item.get('admCode', None)} - 신규 데이터 추가 ===== ")
                    model.objects.create(**item)
    except IntegrityError as e:
        print(f" ===== 에러 : {e} =====")

# 엑셀 저장 로직
def excel(model):
    queryset = model.objects.all()
    data = pd.DataFrame.from_records(queryset.values())
    return data