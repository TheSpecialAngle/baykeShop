from django.views.generic import View
from django.http import JsonResponse
from django.template.response import TemplateResponse

from baykeCore.common.mixin import LoginRequiredMixin
from baykeShop.models import BaykeShopOrderSKUComment



class BaykeCommentView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, )
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        return JsonResponse({'code':'ok', 'message': '评论成功！'})
