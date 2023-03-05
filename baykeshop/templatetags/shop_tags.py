from django.template import Library

from baykeshop.public.forms import SearchForm
from baykeshop.models import BaykePermission, BaykeShopCategory, BaykeBanner
from baykeshop.config.settings import bayke_settings

register = Library()


@register.simple_tag
def navbar_result():
    return BaykeShopCategory.get_cates()


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
    

@register.inclusion_tag(filename="baykeshop/spu_box.html")
def spu_box(spu):
    def skus(spu):
        return spu.baykeshopsku_set.order_by('price')
    
    from django.db.models import Sum
    return {
        'spu': spu,
        'price': skus(spu).first().price,
        'sales': skus(spu).aggregate(Sum('sales'))['sales__sum'],
    }
    

@register.simple_tag
def search(request):
    form = SearchForm(initial=request.GET)
    return form

@register.inclusion_tag(filename="baykeshop/goods/page_list.html")
def page_list(request, page_obj):
    return {
        'page_obj': page_obj,
        'paginator': page_obj.paginator,
        'total': page_obj.paginator.num_pages,
        'current': request.GET.get('page', 1),
        'per_page': page_obj.paginator.per_page,
        # 'tag': tag
    }