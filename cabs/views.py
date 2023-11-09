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
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import base64
from django.utils import timezone

from .utils import car_image_upload

from .serializers import *

from .models import *
from datetime import datetime, timedelta

from django.contrib.auth.hashers import make_password
User = get_user_model()

class CabsViewSet(viewsets.ModelViewSet):
    model = Cars
    serializer_class = CarsSerializer

    def get_queryset(self):
        queryset = Cars.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        serializer = CarsSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Cars.objects.all()
        serializer = CarsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = Cars.objects.get(id=id)
        except Cars.DoesNotExist:
            return Response({"error":"Car does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = CarsSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = CarsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=["post"])
    def upload_images(self, request, *args, **kwargs):
        CAR_IMAGES_KEY = "car_images/{image_name}.jpeg"
        car_id = request.query_params.get("car_id",None)
        if car_id==None:
            return Response({"error":"secondary_id can not be none."}, status=status.HTTP_400_BAD_REQUEST)
        try:
           car = Cars.objects.get(id=car_id)
        except Cars.DoesNotExist:
            return Response({"error":" Cars does not exist with given id."},status=status.HTTP_400_BAD_REQUEST)


        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data.get("image")[0]

        opened_file = file.open()
        base64_file = base64.b64encode(opened_file.read()).decode("utf-8")
        opened_file.close()
        key = CAR_IMAGES_KEY.format(
            image_name=str(car.id)[24:]
            + "-"
            + str(int(timezone.now().timestamp()))
        )

        image_id = car_image_upload(
            car_id=str(car.id),
            base64_file=base64_file,
            key=key,
            file_name=str(file.name),
            file_type=file.content_type,
            file_size=file.size,
        )

        return Response({"message":"image uploaded successfully.","image_id":image_id}, status=status.HTTP_200_OK)


    
class ProfitLossViewSet(viewsets.ModelViewSet):
    model = ProfitLoss
    serializer_class = ProfitLossSerializer

    def get_queryset(self):
        queryset = ProfitLoss.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = ProfitLoss.objects.all()
        serializer = ProfitLossSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)
       
    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CityViewSet(viewsets.ModelViewSet):
    model = City
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        serializer = CitySerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = City.objects.all()
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = City.objects.get(id=id)
        except City.DoesNotExist:
            return Response({"error":"city does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = CitySerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = CitySerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = City.objects.get(id=id)
        except City.DoesNotExist:
            return Response({"error":"city does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response({"message":"City deleted successfully."},status=status.HTTP_200_OK)



class TripsViewSet(viewsets.ModelViewSet):
    model = Trips
    serializer_class = TripsSerializer

    def get_queryset(self):
        queryset = Trips.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        serializer = TripsSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        q = request.query_params.get("q",None)
        if q:
            queryset = Trips.objects.filter(trip_name__icontains=q)
        else:
            queryset=Trips.objects.all()
        serializer = TripsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = Trips.objects.get(id=id)
        except Trips.DoesNotExist:
            return Response({"error":"trip does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = TripsSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = TripsSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TripTimeTableViewSet(viewsets.ModelViewSet):
    model = TripTimeTable
    serializer_class = TripTimeTableSerializer

    def get_queryset(self):
        queryset = Trips.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        serializer = TripTimeTableSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = TripTimeTable.objects.all()
        serializer = TripTimeTableSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = TripTimeTable.objects.get(id=id)
        except TripTimeTable.DoesNotExist:
            return Response({"error":"TripTimeTable does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = TripTimeTableSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = TripTimeTableSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        # id = kwargs.get('pk')
        # try:
        #     queryset = TripTimeTable.objects.get(id=id)
        # except TripTimeTable.DoesNotExist:
        #     return Response({"error":"TripTimeTable does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        # serializer = TripTimeTableSerializer(queryset)
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'])
    def get_trip_table_details(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id==None:
            return Response({"error":"please provide id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = Trips.objects.get(id=id)
        except Trips.DoesNotExist:
            return Response({"error":"trip does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        queryset = TripTimeTable.objects.filter(trip_id=id)
        serializer = TripTimeTableSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    

class BookingViewSet(viewsets.ModelViewSet):
    model = Booking
    serializer_class = BookingSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = Booking.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data

        triptimetable_id = request.data.get('trip')
        customer_id = request.data.get('customer')
        seats = request.data.get('seats')
        try:
            trip = TripTimeTable.objects.get(id=triptimetable_id)
        except TripTimeTable.DoesNotExist:
            return Response({"error":"trip time table does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        

        user_data['total_amount'] = trip.trip.amount * seats
        serializer = BookingSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Booking.objects.all()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data = request.data
        seats = data.get('seats')
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({"error":"Booking does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        total_amount = booking.trip.trip.amount * seats

        data["total_amount"] = total_amount

        serializer = BookingSerializer(booking, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({"error":"Booking does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingDetailsSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_booking_details(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id==None:
            return Response({"error":"please provide id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({"error":"Booking does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def cancel_booking(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id==None:
            return Response({"error":"please provide id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(id=id)
        except Booking.DoesNotExist:
            return Response({"error":"Booking does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        if booking.status == 'cancelled':
            return Response({"error":"Booking already cancelled."},status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'cancelled'
        booking.save()
        return Response({"message":"Booking cancelled Successfully."}, status=status.HTTP_200_OK)




    @action(detail=False, methods=['get'])
    def get_booking_details_by_customer(self, request, *args, **kwargs):
        id = request.query_params.get('id', None)
        if id==None:
            return Response({"error":"please provide id"},status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = Booking.objects.filter(customer_id=id).order_by("-created_at")
        except Booking.DoesNotExist:
            return Response({"error":"Booking does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingHistorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TripStatusViewSet(viewsets.ModelViewSet):
    model = TripStatus
    serializer_class = TripStatusSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        return queryset

    def create(self, request):
        user_data = request.data
        serializer = TripStatusSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = TripStatus.objects.all()
        serializer = TripStatusSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            queryset = TripStatus.objects.get(id=id)
        except TripStatus.DoesNotExist:
            return Response({"error":"TripStatus does not exist with geiven id."},status=status.HTTP_400_BAD_REQUEST)

        serializer = TripStatusSerializer(queryset, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        serializer = TripStatusSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        We can not delete a TripStatus.

        

        
        """
        return Response({},status=status.HTTP_405_METHOD_NOT_ALLOWED)

