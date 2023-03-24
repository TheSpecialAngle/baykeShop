#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :views.py
@说明    :文章视图
@时间    :2023/03/24 15:04:52
@作者    :幸福关中&轻编程
@版本    :1.0
@微信    :baywanyun
'''

from django.views.generic import ListView

from baykeshop.models import BaykeArticle, BaykeArticleCategory, BaykeArticleTags


class ArticleContext:
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = BaykeArticleCategory.objects.all()
        context['tags'] = BaykeArticleTags.objects.all()
        return context
    

class BaykeArticleListView(ArticleContext, ListView):
    """ 文章列表 """

    model = BaykeArticle
    template_name = "baykeshop/article/article_list.html"
    context_object_name = "article_list"
    paginate_by = 15
    
    