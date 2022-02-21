from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ChatGroups(models.Model):
    group_name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ChatGroupUser(models.Model):
    group = models.ForeignKey(ChatGroups, on_delete=models.CASCADE, related_name="group_users", null=True, blank=False)
    users = models.ForeignKey(User, on_delete=models.CASCADE)


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sender", null=True, blank=False)
    receiver = models.ForeignKey(ChatGroups, on_delete=models.CASCADE, related_name="receiver_users", null=True, blank=False)
    text = models.CharField(max_length=200)


EMOTIONS = (
        ('LIKED', 'liked'),
        ('UNLIKE', 'unlike'),
        ('SMILE', 'smile')
    )


class emotions(models.Model):
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name="messages", null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    emotions = models.CharField(max_length=20, choices=EMOTIONS, db_index=True)