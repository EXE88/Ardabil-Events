from rest_framework import serializers
from .models import CreatePost
from django.contrib.auth.models import User

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatePost
        fields = ['id','user','subject_choise','image','title','description','latitude','longitude']

    def validate_user(self,value):
        if User.objects.filter(id=value).exists():
            return value
        raise serializers.ValidationError("user doesnt exists.")
    
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

        return value
    
    def validate_title(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("title cannot be empty.")
        if len(value) > 60:
            raise serializers.ValidationError("title must be less than 60 characters.")
        return value

    def validate_description(self, value):
        if len(value) > 200:
            raise serializers.ValidationError("description must be less than 200 characters.")
        return value

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("longitude must be between -180 and 180.")
        return value