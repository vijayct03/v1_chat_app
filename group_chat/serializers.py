from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ChatGroupUser, ChatGroups, Messages, emotions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroups
        fields = ['created_by', 'group_name', 'id']
        extra_kwargs = {'created_by': {'read_only': True}}


class GroupUserSerializer(serializers.ModelSerializer):
    user_lst = serializers.SerializerMethodField('get_user_group')

    @staticmethod
    def get_user_group(group_obj):
        query_status = group_obj.group_users.all()
        if query_status:
            users = [user.users.username for user in query_status]
            return users

    class Meta:
        model = ChatGroupUser
        fields = ['user_lst']


class CreateMessageSerializer(serializers.ModelSerializer):
    receivers = serializers.SerializerMethodField('get_user_group')
    sender_details = serializers.SerializerMethodField('get_sender')
    group_name = serializers.SerializerMethodField('get_group')

    @staticmethod
    def get_user_group(group_obj):
        query_status = group_obj.receiver.group_users.all()
        if query_status:
            users = [user.users.username for user in query_status]
            return users

    @staticmethod
    def get_sender(group_obj):
        if group_obj:
            return group_obj.sender.username

    @staticmethod
    def get_group(group_obj):
        if group_obj:
            return group_obj.receiver.group_name

    class Meta:
        model = Messages
        fields = ['id', 'sender_details', 'text', 'receivers', 'group_name']
        extra_kwargs = {'sender': {'read_only': True}, 'receiver': {'read_only': True}}


class EmotionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = emotions
        fields = ['user', 'message', 'id', 'emotions']
        extra_kwargs = {'user': {'read_only': True}, 'message': {'read_only': True}}