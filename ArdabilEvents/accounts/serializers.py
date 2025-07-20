from rest_framework import serializers
from .models import UserMetaData
import re

class UserMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMetaData
        fields = ['id', 'user', 'phone_number', 'email']
        read_only_fields = ['user']

    def validate_email(self, value):
        if not re.match(r'^[A-Za-z0-9._%+-]+@gmail\.com$', value):
            raise serializers.ValidationError("Email must be a valid Gmail address and contain only allowed characters.")

        qs = UserMetaData.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This email is already in use.")

        return value

    def validate_phone_number(self, value):
        pattern = r'^9\d{9}$'
        if not re.match(pattern, str(value)):
            raise serializers.ValidationError("Phone number must be 10 digits and start with 9.")

        if not str(value).isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")

        qs = UserMetaData.objects.filter(phone_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This phone number is already in use.")

        return value