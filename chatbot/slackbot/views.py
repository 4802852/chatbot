from rest_framework.views import APIView
from rest_framework.response import Response
from python_weather_api.python_geocoding import xy_geocoding
from python_weather_api.python_weather_api import make_weather_text
from slack.slack import to_slack


class Attend(APIView):
    def post(self, request):
        """
        슬랙에서 채팅 이벤트가 있을 때 호출하는 API
        """

        # 신호 출력
        # print(request.body)

        user = request.data.get("event").get("user")
        channel = request.data.get("event").get("channel")
        text = request.data.get("event").get("text")

        # user 가 봇이 아니고 채널이 날씨 채널인 경우에
        if user != "U029FAZ2AP9" and channel == "C029T1KMBMK":
            # 내용을 띄어쓰기 기준으로 분리
            contents = text.split(" ")
            if contents[-1] == "날씨":
                # 마지막 단어가 "날씨"라면 앞에 주어진 단어로 날씨 데이터 탐색
                place = " ".join(contents[:-1])
                x, y, addr = xy_geocoding(place)
                if addr == None:
                    text = "지역명을 확인해주세요."
                else:
                    text = addr + "\n" + make_weather_text(x, y)
                print(to_slack(text, "#weather"))

        # challenge 데이터 추출하여 Response에 추가
        challenge = request.data.get("challenge")
        return Response(status=200, data=dict(challenge=challenge))
