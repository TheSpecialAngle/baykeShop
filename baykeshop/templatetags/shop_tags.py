from django.template import Library

from baykeshop.models import BaykePermission, BaykeShopCategory, BaykeBanner
from baykeshop.config.settings import bayke_settings

register = Library()

@register.simple_tag
def navbar_result():
    cates = BaykeShopCategory.objects.filter(is_home=True, parent__isnull=True)
    for cate in cates:
        cate.sub_cates = cate.baykeshopcategory_set.filter(is_home=True)
    return cates


@register.inclusion_tag(filename="baykeshop/banner.html")
def banners_result():
    queryset = BaykeBanner.objects.values('id', 'img', 'desc', 'target_url')
    return {'carousels': list(queryset)}


@register.simple_tag
def breadcrumbs(request, opts=None):
    if bayke_settings.ADMIN_MENUS:
        if opts:
            p = BaykePermission.objects.filter(
                permission__content_type__app_label=opts.app_label,
                permission__content_type__model=opts.model_name
            )
            request.breadcrumbs = {
                p.first().menus.name: {
                    'name': str(opts.verbose_name_plural), 
                    'url': request.path
                }
            }
            return request.breadcrumbs
        return request.breadcrumbs
    else:
        return None