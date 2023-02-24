from django import forms


class BaseModelAdmin(metaclass=forms.MediaDefiningClass):
    pass


class ModelAdmin(BaseModelAdmin):
    
    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super().__init__()
    
    def __str__(self):
        return "%s.%s" % (self.model._meta.app_label, self.__class__.__name__)

    def __repr__(self):
        return (
            f"<{self.__class__.__qualname__}: model={self.model.__qualname__} "
            f"site={self.admin_site!r}>"
        )