from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from baykeCore.models import BaykeModelMixin
from baykeShop.models import BaykeShopOrderSKU

User = get_user_model()

class BaykeShopOrderSKUComment(BaykeModelMixin):
    
    class CommentChoices(models.IntegerChoices):
        GOOD = 5, _('好评')
        SO = 3, _('中评')
        BAD = 1, _('差评')

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="用户"
    )
    order_sku = models.ForeignKey(
        BaykeShopOrderSKU, 
        on_delete=models.CASCADE, 
        verbose_name="订单商品"
    )
    content = models.CharField("评价内容", max_length=300)
    comment_choices = models.PositiveSmallIntegerField(
        default=5, 
        choices=CommentChoices.choices,
        verbose_name="评价"
    )
    
    class Meta:
        ordering = ['-add_date']
        verbose_name = "商品评价"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content




