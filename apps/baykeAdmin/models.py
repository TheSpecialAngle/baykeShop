from django.db import models
from django.contrib.auth.models import Permission, Group

# Create your models here.

from baykeCore.models import BaykeModelMixin


class BaykeMenu(BaykeModelMixin):
    """Model definition for BaykeMenus."""
    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True,
        null=True,
        editable=False
    )
    sort = models.PositiveSmallIntegerField(default=1)
    
    # TODO: Define fields here

    class Meta:
        ordering = ['-sort']
        verbose_name = 'BaykeMenu'
        verbose_name_plural = 'BaykeMenus'

    def __str__(self):
        """Unicode representation of BaykeMenus."""
        return self.name


class BaykePermission(BaykeModelMixin):
    """Model definition for Permission."""
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)
    menus = models.ForeignKey(BaykeMenu, on_delete=models.CASCADE)
    icon = models.CharField(max_length=50)
    # TODO: Define fields here

    class Meta:
        verbose_name = '权限规则'
        verbose_name_plural = verbose_name

    def __str__(self):
        """Unicode representation of BaykeMenus."""
        return f"{self.permission.name}  "


