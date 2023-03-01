from django.views.generic import View
from django.http.response import JsonResponse

from baykeshop.forms.shop.user import BaykeUploadModelForm


class WangEditorUploadImg(View):
    
    def post(self, request, *args, **kwargs):
        perms = [
            request.user.is_authenticated,
            request.user.is_active,
            request.user.is_staff,
            request.user.is_superuser,
            request.user.has_perm('baykeshop.add_baykeupload')
        ]
        if not all(perms):
            return JsonResponse({
                "errno": 1,  # 只要不等于 0 就行
                "message": "无权限上传..."
            })
        
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