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
        null=True
    )
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for BaykeMenus."""

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
        """Meta definition for Permission."""

        verbose_name = 'BaykePermission'
        verbose_name_plural = 'BaykePermission'

    def __str__(self):
        """Unicode representation of BaykeMenus."""
        return f"{self.menus.name} - {self.permission.name}"


