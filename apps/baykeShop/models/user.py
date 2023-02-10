from django.db import models
from django.contrib.auth import get_user_model

from baykeCore.models import BaykeModelMixin

User = get_user_model()


class BaykeUserInfo(BaykeModelMixin):
    """一对一扩展的用户模型
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    avatar = models.ImageField(
        "头像", 
        upload_to="avatar/%Y/%m", 
        max_length=200, 
        blank=True, 
        default="avatar/default.jpg"
    )
    nickname = models.CharField(max_length=30, blank=True, default="", verbose_name="昵称")
    phone = models.CharField(max_length=11, blank=True, default="", verbose_name="手机号")
    balance = models.DecimalField("余额", max_digits=8, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname or self.owner.username 

