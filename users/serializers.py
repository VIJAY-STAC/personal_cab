from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "last_login",
            "email",
            "date_of_birth",
            "name",
            "is_active",
            "is_admin",
            "is_staff",
            "role",
            "address",
            "phone_number",
            "password",
            "username"
        )
        extra_kwargs = {'password': {'write_only': True}}