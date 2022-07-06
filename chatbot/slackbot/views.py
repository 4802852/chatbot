from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class Attend(APIView):
    def post(self, request):
        """
        슬랙에서 채팅 이벤트가 있을 때 호출하는 API
        :param request:
        :return:
        """

        # 요청이 어떻게 들어오나 찍어보기
        print(request.body)

        # body에서 challenge 필드만 빼오기
        challenge = request.data.get("challenge")

        user = request.data.get("event").get("user")
        text = request.data.get("event").get("text")
        print("사용자 :", user, "| 메시지 :", text)

        # 응답 데이터로 { challenge : challenge } 주기
        return Response(status=200, data=dict(challenge=challenge))
