from baykeshop.models.admin.user import BaykeUserInfo
from baykeshop.models.admin import BaykeMenu, BaykePermission, BaykeUpload

from baykeshop.models.shop.product import (
    BaykeShopCategory, BaykeShopSPU, BaykeShopSKU, 
    BaykeShopSpecOption, BaykeSPUCarousel
)
from baykeshop.models.shop.spec import BaykeShopSpec, BaykeShopSpecOption
from baykeshop.models.shop.order import BaykeShopOrderInfo, BaykeShopOrderSKU
from baykeshop.models.shop.cart import BaykeShopingCart, BaykeShopAddress
from baykeshop.models.shop.log import BaykeUserBalanceLog
from baykeshop.models.shop.comment import BaykeShopOrderSKUComment

from baykeshop.models.abstract import CarouselAbstractModel


class BaykeBanner(CarouselAbstractModel):
    """ 全局banner模型 """
    
    class Meta:
        verbose_name = '轮播图管理'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.img.name}"