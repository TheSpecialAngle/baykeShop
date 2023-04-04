from django.http.response import JsonResponse
from django.views.generic import View, TemplateView

from baykeshop.config.settings import bayke_settings


class HomeTemplateView(TemplateView):
    """ 商城首页 """
    template_name = "baykeshop/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cates'] = self.get_queryset()
        return context
    
    def get_queryset(self):
        from baykeshop.models import BaykeShopCategory
        from baykeshop.models import BaykeShopSPU
        queryset = BaykeShopCategory.get_cates()
        for cate in queryset:
            cate.spus = BaykeShopSPU.objects.filter(category__in=cate.sub_cates).distinct()[:bayke_settings.HOME_GOODS_COUNT]
        return queryset  


def has_upload_perm(request, perm_codename=None):
    # 权限判断方法
    perms = [
        request.user.is_authenticated,
        request.user.is_active,
        request.user.is_staff,
        request.user.has_perm(f'baykeshop.{perm_codename}') if perm_codename else True
    ]
    return False if not all(perms) else True


class WangEditorUploadImg(View):
    """ 编辑器上传图片接口 """
    def post(self, request, *args, **kwargs):
        if not has_upload_perm(request, 'add_baykeupload'):
            return JsonResponse({
                "errno": 1,  # 只要不等于 0 就行
                "message": "无权限上传..."
            })
        from baykeshop.public.forms import BaykeUploadModelForm
        form = BaykeUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            return JsonResponse({
                "errno": 0, 
                "data": {
                    "url": u.img.url, # 图片 src ，必须
                    "alt": u.img.name, # 图片描述文字，非必须
                    "href": u.img.url # 图片的链接，非必须
                }
            })
        return JsonResponse({"errno": 2, "message": "发生保存错误！"})
    


class TinymceUploadImg(View):
    """ tinymce 编辑器上传图片 """
    from django.views.decorators.csrf import csrf_exempt
    from django.utils.decorators import method_decorator
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        from baykeshop.models import BaykeUpload
        if not has_upload_perm(request, 'add_baykeupload'):
            return JsonResponse({"message": "无权限！"}, status=400)
        if request.FILES:
            from baykeshop.utils import add_upload_file 
            file_name = add_upload_file(request.FILES['file'])
            if file_name:
                baykeupload = BaykeUpload(img=f"{bayke_settings.FILE_PATH}{file_name}")
                baykeupload.save()
                return JsonResponse({'code': 'ok', 'location':f'{baykeupload.img.url}'})
            else:
                return JsonResponse({'code': 'err', 'message': 'error' })
        else:
            return JsonResponse({'code': 'err', 'message': 'qingxuanze' })
