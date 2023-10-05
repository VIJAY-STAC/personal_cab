from rest_framework import serializers
from .models import Cars, ProfitLoss, City, Trips, TripTimeTable, Booking, TripStatus
import pytz
class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = (
            "id",
            'name',
            'milege',
            "driver",
            "image",
        )

class ProfitLossSerializer(serializers.ModelSerializer):
    trip_details = serializers.SerializerMethodField()
    class Meta:
        model = ProfitLoss
        fields = (
            "id",
            'trip_details',
            'investment',
            "returns",
            "profit",
            "loss",
            "business_status"
        )

    def get_trip_details(self, obj):
        trip_details = {
            "name":obj.trip.trip.trip_name,
            "date":obj.trip.trip_date
        }
        return trip_details


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            "id",
            'name',
            'pincode'
        )





class TripsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Trips
        fields = (
            'id',
            'trip_name',
            'start_point',
            'end_point',
            'driver',
            'amount',
            'time',
            'kms',
            'image',
            'image_url'
        )

    def get_image(self, obj):
        # id = str(obj.driver.id)
        # print("****",type(id))
       
        return "ok"


class TripTimeTableSerializer(serializers.ModelSerializer):
    trip_name = serializers.CharField(source='trip.trip_name') 
    start_point= serializers.CharField(source='trip.start_point')
    end_point= serializers.CharField(source='trip.end_point')
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    amt = serializers.SerializerMethodField()

    class Meta:
        model = TripTimeTable
        fields = (
            'id',
            'trip_name',
            'start_point',
            'end_point',
            'date',
            'time',
            "is_active",
            "amt"
        )
    
    def get_date(self, obj):
        ist = pytz.timezone('Asia/Kolkata')
        # covert utc to ist
        utc = (obj.trip_date)
        utc = utc.replace(tzinfo=pytz.UTC)
        date= utc.astimezone(ist)
        return str(date.date())+" "+str(date.time())[:5]

    def get_time(self, obj):
        ist = pytz.timezone('Asia/Kolkata')
        # covert utc to ist
        utc = (obj.trip_date)
        utc = utc.replace(tzinfo=pytz.UTC)
        date= utc.astimezone(ist)
        return date.time()

    
    def get_amt(self, obj):

        return obj.trip.amount    


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            'trip',
            'customer',
            "seats",
            "status",
            "payment_status",
            "total_amount",
            "booking_no"
        )

class BookingHistorySerializer(serializers.ModelSerializer):
    trip_name = serializers.CharField(source='trip.trip.trip_name')
    trip_image = serializers.CharField(source='trip.trip.image_url')
    date = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = (
            "id",
            'trip_name',
            'customer',
            "seats",
            "status",
            "payment_status",
            "total_amount",
            "booking_no",
            "date",
            "trip_image"
        )

    def get_date(self, obj):
        ist = pytz.timezone('Asia/Kolkata')
        # covert utc to ist
        utc = (obj.trip.trip_date)
        utc = utc.replace(tzinfo=pytz.UTC)
        date= utc.astimezone(ist)
        return str(date.date())+" "+str(date.time())[:5]

class BookingDetailsSerializer(serializers.ModelSerializer):
    trip_name = serializers.CharField(source='trip.trip.trip_name')
    date = serializers.SerializerMethodField()
    start_point= serializers.CharField(source='trip.trip.start_point')
    end_point= serializers.CharField(source='trip.trip.end_point')
    pickup_point= serializers.CharField(source='trip.trip.pickup_stop')
    drop_point= serializers.CharField(source='trip.trip.drop_stop')
    car_name = serializers.CharField(source='trip.car.name')
    car_number = serializers.CharField(source='trip.car.car_number')
    duration = serializers.CharField(source='trip.trip.time')
    trip_date = serializers.CharField(source='trip.trip_date')

    class Meta:
        model = Booking
        fields = (
            "id",
            'trip_name',
            'customer',
            "seats",
            "status",
            "payment_status",
            "total_amount",
            "booking_no",
            "date",
            "start_point",
            "end_point",
            "pickup_point",
            "drop_point",
            "car_name",
            "car_number",
            "duration",
            "trip_date"
        )

    def get_date(self, obj):
        ist = pytz.timezone('Asia/Kolkata')
        # covert utc to ist
        utc = (obj.trip.trip_date)
        utc = utc.replace(tzinfo=pytz.UTC)
        date= utc.astimezone(ist)
        return str(date.date())+" "+str(date.time())[:5]



class TripStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripStatus
        fields = (
            'trip',
            'start_time',
            'end_time',
            'trip_status'
        )


