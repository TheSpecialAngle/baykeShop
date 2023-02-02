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
    form = SearchForm()
    category_qs = category_queryset(is_home=True)
    return { 
        'category_qs': category_qs,
        'form': form
    }