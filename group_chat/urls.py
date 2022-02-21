from django.urls import path, re_path

from .views import UserViewSet, GroupView, GroupUserView, MessageView, EmotionsView


app_name = 'group_chat'
urlpatterns = [
    path('users', UserViewSet.as_view(), name="userlist"),
    path('groups', GroupView.as_view(), name="groups"),
    path('group_users/<str:group_name>', GroupUserView.as_view()),
    path('messages/emotion', EmotionsView.as_view()),
    re_path(r'^groups/((?P<group_id>[1-9]+)|(?P<group_name>\w+))/$', GroupView.as_view()),
    path('message/send', MessageView.as_view())
]




