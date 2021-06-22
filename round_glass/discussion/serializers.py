from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from .documents.discussion_documents import *

# class UserDocumentSerializer(DocumentSerializer):
#     class Meta:
#         model = User
#         document = userDocument
#         fields = ('email','phone_number' )
#
#         def get_location(self, obj):
#             try:
#                 return obj.location.to_dict()
#             except:
#                 return {}

class DiscussionDocumentSerializer(DocumentSerializer):
    class Meta:
        model = User
        document = discussionDocument
        fields = ('text','created_at' )

        def get_location(self, obj):
            try:
                return obj.location.to_dict()
            except:
                return {}



class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    mobile_number = serializers.SerializerMethodField(read_only=True)
    tag = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'username', 'email', 'name', 'isAdmin']

    def get_mobile_number(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'mobile_number', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)