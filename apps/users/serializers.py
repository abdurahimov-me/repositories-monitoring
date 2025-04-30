from rest_framework import serializers
from apps.users.models import User
import re


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    number = serializers.CharField()
    city = serializers.CharField()
    arrived = serializers.BooleanField(default=False)
    hobbies = serializers.ListField(child=serializers.CharField(max_length=100), required=False, default=list)

    def validate_number(self, value):
        if not re.match(r'^\+\d{10,15}$', value):
            raise serializers.ValidationError(
                "Telefon raqami + bilan boshlanishi va 10-15 raqamdan iborat bo'lishi kerak.")
        self.user = User.objects.filter(number=value).first()
        if self.user and self.user.is_staff:
            raise serializers.ValidationError("Ushbu nomer ro'yxatdan o'tkan")
        return value

    def create(self, validated_data):
        if self.user:
            return self.user
        # Yangi foydalanuvchini yaratish
        user = User.objects.create_user(
            name=validated_data['name'],
            number=validated_data['number'],
            age=validated_data['age'],
            city=validated_data['city'],
            arrived=validated_data['arrived'],
            hobbies=validated_data['hobbies'],
            password=None  # Agar parol kerak bo'lsa, bu yerda qo'shish mumkin
        )
        return user


class RegisterSerializerVerify(serializers.Serializer):
    code = serializers.CharField()
