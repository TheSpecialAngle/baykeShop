from django.db import models
from baykeCore.models import BaykeModelMixin


class BaykeShopSpecGroup(BaykeModelMixin):
    """规格组
    """
    
    name = models.CharField(max_length=50, verbose_name="规格名称")

    # TODO: Define fields here

    class Meta:
        verbose_name = 'BaykeShopSpecGroup'
        verbose_name_plural = 'BaykeShopSpecGroups'

    def __str__(self):
        return self.name

    # TODO: Define custom methods here


class BaykeShopSpec(BaykeModelMixin):
    """规格
    """

    group = models.ForeignKey(
        BaykeShopSpecGroup, 
        on_delete=models.CASCADE, 
        verbose_name="规格组"
    )
    name = models.CharField(max_length=50, verbose_name="规格")

    # TODO: Define fields here

    class Meta:
        verbose_name = 'BaykeShopSpec'
        verbose_name_plural = 'BaykeShopSpecs'

    def __str__(self):
        return self.name

    # TODO: Define custom methods here


class BaykeShopSpecOption(BaykeModelMixin):
    """
    规格值
    """

    name = models.CharField(max_length=50, verbose_name="规格值")
    spec = models.ForeignKey(BaykeShopSpec, on_delete=models.CASCADE, verbose_name="规格")

    # TODO: Define fields here

    class Meta:
        verbose_name = 'BaykeShopSpecOption'
        verbose_name_plural = 'BaykeShopSpecOptions'

    def __str__(self):
        return self.name

    # TODO: Define custom methods here