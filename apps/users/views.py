from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import RegisterSerializer, RegisterSerializerVerify
from utils.exceptions import BadRequest
from utils.send_message import generate_verification_code, send_verification_code, get_tokens_for_user


class RegisterRequestView(GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        phone_number = serializer.validated_data['number']
        verification_code, exp = generate_verification_code()
        print(verification_code)
        send_verification_code.delay(phone_number, verification_code)  # Asinxron yuborish
        cache.set(f"user id{user.id}", verification_code, exp)
        tokens = get_tokens_for_user(user)
        return Response(
            {"detail": "Tasdiqlash kodi raqamingizga yuborildi!! ",
             "access_token": tokens['access_token'],
             "refresh_token": tokens['refresh_token']
             },
            status=status.HTTP_201_CREATED)


class RegisterVerifyView(GenericAPIView):
    serializer_class = RegisterSerializerVerify
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        user = request.user

        if user.is_staff:
            raise BadRequest("Ro'yxatdan o'tkan")
        checking = cache.get(f"user id{user.id}")
        if not (checking and int(checking) == int(code)):
            raise BadRequest("Kod eskirgan yoki xato kod kiritilmoqda ")
        user.is_staff = True
        user.save()

        return Response({
            "details": "Successfull"},
            status=status.HTTP_200_OK
        )
