from django.contrib import admin

from baykeshop.public.sites import bayke_site
from baykeshop.public.admin import BaseModelAdmin
from baykeshop.models import BaykeArticle, BaykeArticleCategory, BaykeArticleTags


@admin.register(BaykeArticleCategory, site=bayke_site)
class BaykeArticleCategoryAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('name', 'icon', 'desc', 'add_date')
    search_fields = ('name', 'desc')


@admin.register(BaykeArticle, site=bayke_site)
class BaykeArticleAdmin(BaseModelAdmin):
    '''Admin View for BaykeArticleCategory'''

    list_display = ('title', 'category', 'add_date')
    search_fields = ('title', 'desc')
    
    def save_model(self, request, obj, form, change) -> None:
        obj.owner = request.user
        return super().save_model(request, obj, form, change)
    

bayke_site.register(BaykeArticleTags)