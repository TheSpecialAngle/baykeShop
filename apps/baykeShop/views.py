from django.shortcuts import render
from django.views.generic import View
from django.template.response import TemplateResponse
# Create your views here.

class HomeView(View):
    
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, 'baykeShop/index.html', context={})
