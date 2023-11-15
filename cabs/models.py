
import uuid
from django.db import models
from django.conf import settings

from users.models import User



BOOKING_STATUS = (
    ("waiting","waiting"),
    ("confirmed","confirmed"),
    ("cancelled","cancelled"),
)

PAYMENT_STATUS = (
    ("unpaid","unpaid"),
    ("paid","paid")
)



TRIP_STATUS = (
    ("completed","completed"),
    ("started","started"),
    ("scheduled","scheduled"),
    ("cancelled","cancelled"),
)

BUSINESS_STATUS = (
    ("profit","profit"),
    ("loss","loss")
  
    
)

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True



class PrimaryUUIDModel(models.Model):
    # id = models.AutoField(primary_key=True,)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    
    class Meta(object):
        abstract = True


class PrimaryUUIDTimeStampedModel(PrimaryUUIDModel, TimeStampedModel):
    class Meta(object):
        abstract = True


class File(PrimaryUUIDTimeStampedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=120, null=False, blank=False)
    key = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(blank=False, null=False)
    size = models.PositiveIntegerField(default=0)
    file_type = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.url

class Cars(PrimaryUUIDTimeStampedModel):
    name = models.CharField(max_length=50, blank=False)
    milege = models.DecimalField(max_digits=1000,decimal_places=2, blank=True)
    passanger_seats = models.IntegerField(default=4)
    driver = models.ForeignKey(
    User, 
    blank=False,
    on_delete=models.CASCADE,
    related_name='car_user',
    )
    image = models.ImageField(upload_to='cars/', blank=True)
    imgae_url = models.CharField(max_length=50000, blank=True)
    car_number = models.CharField(max_length=50, blank=True)
    car_images = models.ManyToManyField(File, related_name="car_images", null=True, blank=True)
    review = models.CharField(max_length=50, blank=True, null=True )
    review2 = models.CharField(max_length=50, blank=True, null=True )

    def __str__(self):
        return self.name


class City(PrimaryUUIDTimeStampedModel):
    name = models.CharField(max_length=50, blank=False)
    pincode = models.CharField(max_length=6, blank=False)
    def __str__(self):
        return self.name

class Trips(PrimaryUUIDTimeStampedModel):

    trip_name = models.CharField(max_length=100, blank=False)

    start_point =models.ForeignKey(
                    City, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='city_start_point',
                    )
    end_point = models.ForeignKey(
                    City, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='city_end_point',
                    )
    driver = models.ForeignKey(
                    User, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='trip_user',
                    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    time = models.IntegerField( blank=True)
    kms = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    image_url = models.CharField(max_length=50000, blank=True)
    pickup_stop = models.CharField(max_length=50000, blank=True)
    drop_stop = models.CharField(max_length=50000, blank=True)
    def __str__(self):
        return self.trip_name

class TripTimeTable(PrimaryUUIDTimeStampedModel):
    trip = models.ForeignKey(
                    Trips, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='trip_table',
                    )
    trip_date = models.DateTimeField(blank=False)
    is_active = models.BooleanField(default=True)
    car = models.ForeignKey(
                    Cars,
                    null=True,  # change it to False 
                    on_delete=models.CASCADE,
                    related_name='car_trip',
                    )
    driver = models.ForeignKey(
                    User,
                    null=True,
                    on_delete=models.CASCADE,
                    related_name='driver_trip',
                    )

    def __str__(self):
        return self.trip.trip_name +" "+ str(self.trip_date)

class Booking(PrimaryUUIDTimeStampedModel):
    booking_no =models.IntegerField(default=1) 
    trip = models.ForeignKey(
                    TripTimeTable, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='bokking_trip',
                    )
    customer = models.ForeignKey(
                    User, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='customer_user',
                    )
    seats = models.IntegerField(default=1) 
    status = models.CharField(max_length=100,choices=BOOKING_STATUS, default='waiting')
    payment_status = models.CharField(max_length=100,choices=PAYMENT_STATUS, default='unpaid')
    total_amount = models.DecimalField(max_digits=100,decimal_places=2, blank=False, default=0.0 )

   

    def __str__(self):
        return str(self.booking_no)

class TripStatus(PrimaryUUIDTimeStampedModel):
    trip = models.ForeignKey(
                    TripTimeTable, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='trip_status',
                    )
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    trip_status = models.CharField(max_length=100,blank=False,choices=TRIP_STATUS, default='scheduled')
    def __str__(self):
        return self.trip.trip.trip_name


    
class ProfitLoss(PrimaryUUIDTimeStampedModel):
    trip = models.ForeignKey(
                    TripTimeTable, 
                    blank=False,
                    on_delete=models.CASCADE,
                    related_name='pl_status',
                    )
    investment = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    returns = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    profit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    loss = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    business_status = models.CharField(max_length=100,blank=True,choices=BUSINESS_STATUS, default='profit')

    def save(self, *args, **kwargs):

        if self.investment < self.returns:
            self.profit = self.returns - self.investment
        else:
            self.profit = 0.0

        if self.investment > self.returns:
            self.loss = self.investment - self.returns
        else:
            self.loss = 0.0

        if self.profit < self.loss:
            self.business_status='loss'
        else:
            self.business_status='profit'
        super().save(*args, **kwargs)  


