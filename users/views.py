from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .utils import generate_otp_and_key, send_custom_email, verify_otp


from .serializers import UserSerializer

from .models import User
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        user_data['password']=make_password(user_data['password'])
        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"message": f"User does not exist with given email."}, status=status.HTTP_400_BAD_REQUEST)

            if not user.check_password(password):
                return Response({"message": "incorrect credentials"}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)

            user_details = {
                'id': user.id,
                'access_token': str(refresh.access_token),
                'stat': True,
	            'message': "Login successful"
                
            }

            return Response(user_details, status=status.HTTP_200_OK)
        except KeyError:
            res = {'error': 'Please provide an email and a password'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post'])
    def forgot_password(self, request, *args, **kwargs):
        PASSWORD_RESET_KEY = "user_password_reset_key.{otp_key}"
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": f"user with {email} is not registered."}, status=status.HTTP_400_BAD_REQUEST)

        otp, otp_key = generate_otp_and_key(
            uuid=user.id, secret_key=PASSWORD_RESET_KEY)

        if cache.get(otp_key) is not None:
            otp = cache.get(otp_key)

        print(otp)

        if len(str(otp)) > 6:
            otp = str(otp)[:6]

        send_custom_email("OTP from todo app.", f"Your One time Password is : {otp}", [user.email])

        cache.set(otp_key, otp, 300)
        return Response("OTP sent on registered email id.", status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return None

    @action(detail=False, methods=["post"], permission_classes=[])
    def set_new_password(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        otp = request.data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": f"user with {email} is not registered."}, status=status.HTTP_400_BAD_REQUEST)

        response, otp_key = verify_otp(user_id=user.id, otp=otp)

        if otp_key is None:
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save(update_fields=["password"])
        cache.delete(otp_key)

        return Response({"message":"Password changed succesfully."}, status=status.HTTP_200_OK)

   