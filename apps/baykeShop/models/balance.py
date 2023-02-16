from django.db import models
from django.contrib.auth import get_user_model

from baykeCore.models import BaykeModelMixin

User = get_user_model()


class BaykeUserBalanceLog(BaykeModelMixin):
    """ 用户余额变动表
    """
    class BalanceChangeStatus(models.IntegerChoices):
        # 收支状态
        ADD = 1    # 增加
        MINUS = 2  # 支出
    
    class BalanceChangeWay(models.IntegerChoices):
        # 收支渠道或方式
        PAY = 1     # 线上充值
        ADMIN = 2   # 管理员手动更改
        SHOP = 3    # 余额抵扣商品
    
    owner = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    amount = models.DecimalField("金额", max_digits=15, decimal_places=2)
    change_status = models.PositiveSmallIntegerField(
        choices=BalanceChangeStatus.choices, 
        blank=True,
        null=True
    )
    change_way = models.PositiveSmallIntegerField(
        choices=BalanceChangeWay.choices, 
        default=BalanceChangeWay.ADMIN        # 默认为后台
    )

    # TODO: Define fields here

    class Meta:
        verbose_name = '余额明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.owner.username}-{self.amount}"

    @property
    def changestatus(self):
        if self.change_status == 1:
            return "增加"
        if self.change_status == 2:
            return "支出"
        
    @property
    def changeway(self):
        if self.change_way == 1:
            return "线上充值"
        if self.change_way == 2:
            return "管理员手动更改"
        if self.change_way == 3:
            return "购买商品抵扣"