import code
from email import message
from rest_framework import views
from sqlalchemy import true
from cv001.utils.utils import get_JWT_token, get_uid
from user.models import user
from doctors.models import doctor, office
from rest_framework.response import Response
from rest_framework import status
from cv001.messages import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from cv001.utils.utils import rettime
from sos import models
from user.utils.jwt import *


class sosView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            phone = request.data["pno"]
            lon = request.data["long"]
            lat = request.data["lat"]
            jwt = sos_jwt(phone)
            instance = models.guest_sos.objects.create(
                pno=phone, long=lon, lat=lat, token=jwt)

            response = {
                'success': True,
                'data': {
                    'token': jwt,
                    'code': 200,
                    'message': 'SOS request sent successfully'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


class updateView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            token = request.data["token"]
            lon = request.data["long"]
            lat = request.data["lat"]
            uid = sos_decode(token)
            if uid:
                instance = models.update_quads.objects.create(
                    long=lon, lat=lat, token=token)
                response = {
                    'success': True,
                    'data': {
                        'code': 200,
                        'message': 'coordinates updated successfully'

                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
