from django.db import models
from django.urls import reverse

# Create your models here.
from baykeCore.models import BaykeModelMixin, BaykeCategoryMixin, BaykeCarouselMixin
from .spec import BaykeShopSpecOption


class BaykeShopCategory(BaykeCategoryMixin):
    """商品分类
    """
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
    )
    
    is_home = models.BooleanField(
        default=False, 
        verbose_name="是否推荐", 
        help_text="如果为True则推荐到首页楼层及出现在导航菜单"
    )

    # TODO: Define fields here

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name 


class BaykeShopSPU(BaykeModelMixin):
    """SPU
    """

    title = models.CharField("商品名称", max_length=150)
    keywords = models.CharField("商品关键字", max_length=150, blank=True, default="")
    desc = models.CharField("商品描述", max_length=200, blank=True, default="")
    category = models.ManyToManyField(BaykeShopCategory, verbose_name="商品分类")
    unit = models.CharField("单位", max_length=50)
    cover_pic = models.ImageField("封面图", upload_to="product/cover/spu/%Y/%m", max_length=200)
    freight = models.DecimalField("运费", max_digits=5, decimal_places=2, blank=True, default=0.00)
    content = models.TextField("商品详情")

    # TODO: Define fields here

    class Meta:
        verbose_name = '商品管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class BaykeShopSKU(BaykeModelMixin):
    """sku
    """
    spu = models.ForeignKey(BaykeShopSPU, on_delete=models.CASCADE, verbose_name="商品")
    options = models.ManyToManyField(BaykeShopSpecOption, blank=True, verbose_name="商品规格")
    cover_pic = models.ImageField(
        "封面图", 
        upload_to="cover/sku/%Y/%m", 
        max_length=200,
        blank=True,
        null=True
    )
    price = models.DecimalField("售价", max_digits=8, decimal_places=2)
    cost_price = models.DecimalField("成本价", max_digits=8, decimal_places=2)
    org_price = models.DecimalField("原价", max_digits=8, decimal_places=2)
    stock = models.IntegerField("库存", default=0)
    sales = models.PositiveIntegerField("销量", default=0, editable=False)
    numname = models.CharField("商品编号", max_length=50, default="", blank=True)
    weight = models.FloatField("重量(KG)", default=0, blank=True)
    vol = models.FloatField("体积(m³)", default=0, blank=True)

    # TODO: Define fields here

    class Meta:
        verbose_name = 'BaykeShopSKU'
        verbose_name_plural = 'BaykeShopSKUs'

    def __str__(self):
        return self.spu.title


class BaykeSPUCarousel(BaykeCarouselMixin):
    """
    spu轮播图
    """
    product = models.ForeignKey(BaykeShopSPU, on_delete=models.CASCADE)
    # TODO: Define fields here

    class Meta:
        verbose_name = 'BaykeSPUCarousel'
        verbose_name_plural = 'BaykeSPUCarousels'

    def __str__(self):
        return f"{self.img.name}"

    # TODO: Define custom methods here


class BaykeShopBanner(BaykeCarouselMixin):
    
    class Meta:
        verbose_name = '轮播图管理'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.img.name}"