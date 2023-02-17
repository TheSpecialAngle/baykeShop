from django.template import Library
from django.urls import resolve, reverse
from baykeShop.models import BaykeShopCategory, BaykeShopBanner, BaykeShopingCart
from baykeShop.forms import SearchForm


register = Library()


def category_queryset(is_home=None):
    """
    当参数is_home为None时返回所有的分类数据
    当传递给is_home值为布尔值True或False时返回该字段对应的数据
    """
    queryset = BaykeShopCategory.objects.show()
    if is_home is not None:
        queryset = queryset.filter(is_home=is_home)
    return queryset


@register.inclusion_tag('baykeShop/navbar.html', takes_context=True)
def navbar_result(context):
    # 导航模块
    form = SearchForm(context["request"].GET)
    category_qs = category_queryset(is_home=True)
    return { 
        'category_qs': category_qs,
        'form': form
    }
    

@register.inclusion_tag('baykeShop/carousel.html')
def carousel_result():
    # 轮播图模块
    queryset = BaykeShopBanner.objects.show().values('id', 'img', 'desc', 'target_url')
    return {
        'carousels': list(queryset)
    }


@register.inclusion_tag('baykeShop/page.html', takes_context=True)
def page_result(context, page_obj, *args, **kwargs):
    """分页组件
    使用方法
        {% load shop_tags %}
        {% page_result page_obj tag=pay_satus %} 
    接受参数：
        page_obj 分页后的queryset
        tag为关键字参数，当你要为特定的查询条件数据进行分页时使用
        那么tag的值pay_satus的数据格式应为: `a=1&b=2`或者None这种方式
    """
    request = context['request']
    current = request.GET.get('page', 1)
    tag=""
    if kwargs and kwargs['tag']:
        tag = kwargs['tag']
    return {
        'paginator': page_obj.paginator,
        'total': page_obj.paginator.num_pages,
        'current': current,
        'per_page': page_obj.paginator.per_page,
        'tag': tag
    }
    

@register.simple_tag
def cart_num(user):
    return BaykeShopingCart.get_cart_count(user) if user.is_authenticated else 0