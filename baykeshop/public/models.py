from baykeshop.public.abstract import CarouselAbstractModel

class BaykeBanner(CarouselAbstractModel):
    """ 全局banner模型 """
    
    class Meta:
        verbose_name = '轮播图管理'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.img.name}"