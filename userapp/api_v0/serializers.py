from django.contrib.auth import get_user_model
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        user = get_user_model().objects.create(username=validated_data["email"])
        user.set_password(validated_data["password"])
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data.get("last_name", "")
        user.email = validated_data["email"]
        user.phone_number = validated_data.get("phone_number", "")
        user.address = validated_data.get("address", "")
        user.save()
        return user
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "address", "phone_number", "password", "username")


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)

    class Meta:
        model = get_user_model()
        fields = ("username","password")


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=1000)
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "first_name", "last_name", "address", "phone_number", "username")

