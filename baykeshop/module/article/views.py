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

from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from baykeshop.models import BaykeArticle, BaykeArticleCategory, BaykeArticleTags


class ArticleContext:
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = self.get_cates()
        context['tags'] = self.get_tags()
        # context['archive'] = BaykeArticle.get_archive()
        context['tags_classes'] = ['is-danger', 'is-info', 'is-success', 'is-primary', 'is-light', 'is-black']
        return context
    
    def get_cates(self):
        return BaykeArticleCategory.objects.all()
    
    def get_tags(self):
        return BaykeArticleTags.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        for qs in queryset:
            qs.pv = self.get_stats(qs.id).pv
            qs.uv = self.get_stats(qs.id).uv
        return queryset
    
    def get_stats(self, object_id):
        return BaykeArticle.get_stats(self.request, object_id)
    

class BaykeArticleListView(ArticleContext, ListView):
    """ 文章列表 """

    model = BaykeArticle
    template_name = "baykeshop/article/article_list.html"
    paginate_by = 15
    

class BaykeArticleDetailView(ArticleContext, DetailView):
    """ 文章详情 """
    model = BaykeArticle
    template_name = "baykeshop/article/article_detail.html"
    context_object_name = "article"
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.pv = self.get_stats(obj.id).pv
        obj.uv = self.get_stats(obj.id).uv
        return obj
    

class BaykeArticleCategoryListView(ArticleContext, SingleObjectMixin, ListView):
    """ 分类文章列表 """

    paginate_by = 15
    template_name = "baykeshop/article/article_list.html"
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.get_cates())
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cate'] = self.object
        return context
    
    def get_queryset(self):
        queryset = self.object.baykearticle_set.all()
        for qs in queryset:
            qs.pv = self.get_stats(qs.id).pv
            qs.uv = self.get_stats(qs.id).uv
        return queryset
    
    

    