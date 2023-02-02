from django.template import Library
from baykeShop.models import BaykeShopCategory
from baykeShop.forms import SearchForm

register = Library()


def category_queryset(is_home=None):
    """
    当参数is_home为None时返回所有的分类数据
    当传递给is_home值为布尔值True或False时返回该字段对应的数据
    """
    queryset = BaykeShopCategory.objects.all()
    if is_home is not None:
        queryset = queryset.filter(is_home=is_home)
    return queryset


@register.inclusion_tag('baykeShop/navbar.html')
def navbar_result():
    # 导航模块
    form = SearchForm()
    category_qs = category_queryset(is_home=True)
    return { 
        'category_qs': category_qs,
        'form': form
    }
    

@register.inclusion_tag('baykeShop/carousel.html')
def carousel_result():
    # 轮播图模块
    return {
        'carousels': [
            { 'text': 'Slide 1', 'color': 'primary' },
            { 'text': 'Slide 2', 'color': 'info' },
            { 'text': 'Slide 3', 'color': 'success' },
            { 'text': 'Slide 4', 'color': 'warning' },
            { 'text': 'Slide 5', 'color': 'danger' }
        ]
    }
    

def sku(spu, only=False):
    """
    spu为一个商品spu对象
    only为Flase返回当前spu下的sku的queryset
    only为True返回当前spu下的sku的首个对象
    """
    skus = spu.baykeshopsku_set.all()
    if skus.exists() and only is True:
        return skus.first()
    return skus


@register.filter
def sku_price(spu, price=None):
    """
    spu为一个商品spu对象
    price参数默认为None,当传入值与商品的价位相关的字段名称对应时返回对应的价位
    """
    if price == 'cost_price':
        price = sku(spu, only=True).cost_price
    if price == 'org_price':
        price = sku(spu, only=True).org_price
    else:
        price = sku(spu, only=True).price
    return price
