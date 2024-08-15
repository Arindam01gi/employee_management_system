from .models import User,UserDetails,Post
from rest_framework import serializers
from .utils import upload_to_google_drive
from django.utils import timezone
import os,logging


logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username','active']

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['user_id', 'firstname', 'lastname', 'email', 'phone', 'user_role', 'profile_pic', 'designation', 'salary', 'joining_date', 'created_on', 'updated_on']
        
class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Post
        fields = ['description', 'user_id']

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(pk=user_id)
        post = Post.objects.create(user=user, **validated_data)
        return post
        
    # def create(self,validated_data):
    #     doc_location = validated_data.get('doc_loaction')
    #     try:
    #         google_drive_file_id = upload_to_google_drive(doc_location, os.path.basename(doc_location))
    #         doc_location = f"https://drive.google.com/file/d/{google_drive_file_id}/view"
    #     except Exception as e:
    #         logger.info("logger in exception")
    #         raise serializers.ValidationError(f"Failed to upload file to Google Drive: {str(e)}")
        
    #     post = Post.objects.create(
    #         description=validated_data.get('description'),
    #         doc_loaction=doc_location,
    #         created_on=validated_data.get('created_on', timezone.now()),
    #         updated_on=validated_data.get('updated_on', timezone.now())
    #     )
    #     return post
