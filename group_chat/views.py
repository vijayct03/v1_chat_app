import http
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer, GroupUserSerializer, CreateMessageSerializer, EmotionsSerializer
from rest_framework.response import Response
from .models import ChatGroups, ChatGroupUser, Messages
from rest_framework import status
from django.db.models import Q

class UserViewSet(APIView):

    def get(self, request, user_id=None):
        if not user_id:
            queryset = User.objects.filter(is_superuser=False)
            serializer_class = UserSerializer(queryset, many=True)
        else:
            queryset = User.objects.filter(pk=user_id).first()
            if not queryset:
                return Response("Requested User not found.", status=status.HTTP_404_NOT_FOUND)
            serializer_class = UserSerializer(queryset)
        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self,request):
        current_user = request.user
        if current_user.is_superuser:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        return Response("User doesn't have Permission.", status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        current_user = request.user
        user_id = request.query_params.get('user_id', None)
        user_name = request.query_params.get('user_name', None)
        if current_user.is_superuser:
            if user_id:
                instance = User.objects.get(id=user_id)
            elif user_name:
                instance = User.objects.get(username=user_name)
            serializer = UserSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.update(instance, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("User doesn't have Permission.",status=status.HTTP_401_UNAUTHORIZED)


class GroupView(APIView):

    def get(self, request, group_id=None, group_name=None):
        if group_id:
            queryset = ChatGroups.objects.get(id=group_id)
            serializer_class = GroupSerializer(queryset)
        elif group_name:
            queryset = ChatGroups.objects.filter(group_name=group_name).first()
            serializer_class = GroupSerializer(queryset)
        else:
            queryset = ChatGroups.objects.all()
            serializer_class = GroupSerializer(queryset, many=True)

        return Response(serializer_class.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer1 = GroupSerializer(data=request.data)
        if serializer1.is_valid():
            serializer1.save(created_by=request.user)
            group = ChatGroups.objects.get(group_name=serializer1.validated_data.get('group_name'))
            ChatGroupUser.objects.create(group=group, users=request.user)
            return Response(serializer1.data, status=status.HTTP_200_OK)

    def delete(self, request, group_id=None, group_name=None):
        obj = ChatGroups.objects.filter(Q(id=group_id) | Q(group_name=group_name))
        if obj:
            obj.delete()
            return Response("Group Deleted successfully.", status=status.HTTP_200_OK)
        return Response("Error while delete.", status=status.HTTP_400_BAD_REQUEST)


class GroupUserView(APIView):

    def get(self,request, group_name):
        cur_group = ChatGroups.objects.get(group_name=group_name)
        if cur_group:
            # group_users = ChatGroupUser.objects.filter(group=cur_group)
            serializer = GroupUserSerializer(cur_group)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, group_name):
        name = request.query_params.get('user', None)
        user_obj = User.objects.filter(username=name).first()
        cur_group = ChatGroups.objects.get(group_name=group_name)
        if user_obj and cur_group:
            ChatGroupUser.objects.create(users=user_obj, group=cur_group)
            return Response(f"{name} User Added in the {group_name} group.", status=status.HTTP_200_OK)


class MessageView(APIView):

    def post(self, request):
        name = request.query_params.get('group_name', None)
        if name:
            cur_group = ChatGroups.objects.get(group_name=name)
            serializer = CreateMessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(sender=request.user, receiver=cur_group)
                return Response(serializer.data, status=status.HTTP_200_OK)


class EmotionsView(APIView):

    def post(self, request):
        message_id = request.query_params.get('msg_id', None)
        if message_id:
            message = Messages.objects.get(pk=message_id)
            serializer = EmotionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(message=message, user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)