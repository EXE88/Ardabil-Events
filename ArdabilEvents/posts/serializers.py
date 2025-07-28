from rest_framework import serializers
from .models import CreatePost
from django.contrib.auth.models import User
from django.utils.html import strip_tags
import os
from PIL import Image

class CreatePostSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['subject_choise'].read_only = True

    class Meta:
        model = CreatePost
        fields = ['id','user','subject_choise','image','title','description','latitude','longitude']
        read_only_fields = ['user']
        
    def validate_subject_choise(self,value):
        if str(value) in dict(CreatePost.Subject.choices):
            return value
        raise serializers.ValidationError("selected item is not in the choices")
    
    def validate_image(self, value):
        max_size_mb = 10
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError("image size must be less than 10MB")
        
        if value.content_type not in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError("file type is not allowed.")
        
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise serializers.ValidationError("Only .jpg and .png files are allowed.")

        try:
            img = Image.open(value)
            img.verify()
        except Exception:
            raise serializers.ValidationError("Uploaded file is not a valid image.")

        return value
    
    def validate_title(self, value):
        if value != strip_tags(value):
            raise serializers.ValidationError("malicious request detected.")
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("title cannot be empty.")
        if len(value) > 60:
            raise serializers.ValidationError("title must be less than 60 characters.")
        return value

    def validate_description(self, value):
        if value != strip_tags(value):
            raise serializers.ValidationError("malicious request detected.")
        if len(value) > 200:
            raise serializers.ValidationError("description must be less than 200 characters.")
        return value

    def validate_latitude(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("latitude must be a number.")
        if value < -90 or value > 90:
            raise serializers.ValidationError("latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError("longitude must be a number.")
        if value < -180 or value > 180:
            raise serializers.ValidationError("longitude must be between -180 and 180.")
        return value