from django.http import JsonResponse
import requests

def api(name, admCode):
        api_url = "https://api.vworld.kr/ned/data/"+name

        jsonp_params = {
            'key': '56C7879D-F177-3925-83BE-62B81A40452E',
            "domain": "http://localhost:3000/",
            "format": "json",
            "numOfRows": "5000",
            "pageNo": "1"
        }

        if admCode:
            jsonp_params["admCode"] = admCode

        response = requests.get(api_url, params=jsonp_params)

        if response.status_code == 200:
            data = data = response.json()
            return data.get('admVOList', {}).get('admVOList', None)
        else:
            return JsonResponse({'에러'}, status=500)
    
def main(request):
    print("main")
    admCodeList= []
    admSiList=[]
    admDongList=[]
    admReeList=[]

    # # 시도 리스트 구하기
    # print("시도 리스트 구하기")
    # admCodeList = api("admCodeList", None)

    # # 시군구 리스트 구하기
    # print("시군구 리스트 구하기")
    # for item in admCodeList:
    #     list= api("admSiList", item.get('admCode', None))
    #     if list:
    #         admSiList.extend(list)

    # # 읍면동 리스트 구하기
    # print("읍면동 리스트 구하기")
    # for item in admSiList:
    #     list= api("admDongList", item.get('admCode', None))
    #     if list:
    #         admDongList.extend(list)

    # # 리 리스트 구하기
    # print("리 리스트 구하기")
    # for item in admDongList:
    #     list= api("admReeList", item.get('admCode', None))
    #     if list:
    #         admReeList.extend(list)

    # return JsonResponse(admDongList, safe=False)

    list= api("admReeList", 52720400)
    print(f"list : {list}")
    if list:
         admReeList.extend(list)

    return JsonResponse(admReeList, safe=False)

if __name__ == "__main__":
    main("main")