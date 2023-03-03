from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    """ 商城首页 """
    
    template_name = "baykeshop/index.html"