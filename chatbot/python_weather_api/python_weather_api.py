from collections import defaultdict
import enum
import os, json, requests
from datetime import datetime, timedelta
from urllib.parse import urlencode, unquote, quote_plus

path = os.path.dirname(os.path.abspath(__file__))

sky_code = {"1": "맑음", "3": "구름많음", "4": "흐림"}
pty_code = {
    "0": "-",
    "1": "비",
    "2": "비/눈",
    "3": "눈",
    "5": "빗방울",
    "6": "빗방울눈날림",
    "7": "눈날림",
}

# token을 secrets.json 파일로부터 읽어오는 함수
def get_token():
    try:
        secret_file = path + "\secrets.json"
        with open(secret_file) as f:
            secrets = json.loads(f.read())
        token = secrets["token"]
        return token
    except:
        return False


# 초단기예보 정보 요청
def get_ultra_srt_fcst(x, y):
    token = get_token()
    if not token:
        print("no token")
        return False
    callback_url = (
        "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"
    )
    # base_date, base_time 계산
    time_now = datetime.now()
    if time_now.minute < 45:
        time_target = time_now.replace(minute=30) - timedelta(hours=1)
    else:
        time_target = time_now.replace(minute=30)
    base_date = time_target.strftime("%Y%m%d")
    base_time = time_target.strftime("%H%M")
    params = "?" + urlencode(
        {
            quote_plus("serviceKey"): token,  # 인증키
            quote_plus("numOfRows"): "60",  # 한 페이지 결과 수 // default : 10
            quote_plus("pageNo"): "1",  # 페이지 번호 // default : 1
            quote_plus("dataType"): "JSON",  # 응답자료형식 : XML, JSON
            quote_plus("base_date"): base_date,  # 발표일자 // yyyymmdd
            quote_plus("base_time"): base_time,  # 발표시각 // HHMM, 매 시각 45분 이후 호출
            quote_plus("nx"): x,  # 예보지점 X 좌표
            quote_plus("ny"): y,  # 예보지점 Y 좌표
        }
    )
    res = requests.get(callback_url + unquote(params))
    items = res.json().get("response").get("body").get("items").get("item")

    weather_data = defaultdict(dict)
    for item in items:
        fcstTime = item["fcstTime"][:2] + "시"
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item["category"] == "SKY":
            weather_data[fcstTime]["sky"] = sky_code[item["fcstValue"]]
        # 1시간 동안 강수량
        if item["category"] == "RN1":
            weather_data[fcstTime]["rain"] = item["fcstValue"]
        # 강수형태 : 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item["category"] == "PTY":
            weather_data[fcstTime]["pty"] = pty_code[item["fcstValue"]]
    return weather_data


def make_weather_text(x, y):
    w_data = get_ultra_srt_fcst(x, y)
    text = ""
    for i, key in enumerate(w_data.keys()):
        text += key + ": "
        text += w_data[key]["sky"] + "/"
        text += w_data[key]["pty"] + "/"
        text += w_data[key]["rain"]
        if i != 5:
            text += "\n"
    return text


def main():
    # data = get_ultra_srt_fcst(60, 127)
    make_weather_text(60, 127)


if __name__ == "__main__":
    main()
