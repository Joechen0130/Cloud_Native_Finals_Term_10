from turtle import title
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.urls import reverse
from cryptography.fernet import Fernet
from django.conf import settings
import base64, os
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import Group

from django_prometheus.models import ExportModelOperationsMixin
# Create your models here.
# users_in_group = Group.objects.get(name="group name").user_set.all()
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='uploads/',blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    #try history log 
    history = HistoricalRecords() # new line
    # group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    # 修改的時間放這
    def __str__(self):
        return self.user.username + '-' + self.title

    def get_share_url(self):
        fernet = Fernet(settings.ID_ENCRYPTION_KEY)
        value = fernet.encrypt(str(self.pk).encode())
        value = base64.urlsafe_b64encode(value).decode()
        return reverse("share-file-id", kwargs={"id": (value)})
    # 可以試著用城市去確定權限 https://ithelp.ithome.com.tw/articles/10212466?sc=pt (用shell 去做)
    # class Meta:
    #     change_time = ['date_created']
    #     permissions = (("can_view", "view")
    #                    , #查看文件
    #     )     

@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)
# 拿掉原本修改的
@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file_path
    except sender.DoesNotExist:
        return False

    new_file = instance.file_path
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


# class Post(ExportModelOperationsMixin('file'), models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     description = models.TextField(blank=True, null=True)
#     file_path = models.FileField(upload_to='uploads/',blank=True, null=True)
#     date_created = models.DateTimeField(default=timezone.now)
#     date_updated = models.DateTimeField(auto_now=True)
#     #try history log 
#     history = HistoricalRecords() # new line
#     # group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
#     # 修改的時間放這
#     def __str__(self):
#         return self.user.username + '-' + self.title

#     def get_share_url(self):
#         fernet = Fernet(settings.ID_ENCRYPTION_KEY)
#         value = fernet.encrypt(str(self.pk).encode())
#         value = base64.urlsafe_b64encode(value).decode()
#         return reverse("share-file-id", kwargs={"id": (value)})
#     # 可以試著用城市去確定權限 https://ithelp.ithome.com.tw/articles/10212466?sc=pt (用shell 去做)
#     # class Meta:
#     #     change_time = ['date_created']
#     #     permissions = (("can_view", "view")
#     #                    , #查看文件
#     #     )   