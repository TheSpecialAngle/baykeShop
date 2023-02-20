import csv
from django.http.response import HttpResponse
from django.utils.html import format_html
from django.urls import reverse


class CustomActions:
    """ 自定义动作 """
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv', charset='GB2312')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "导出CSV"
    
    def mark_delete(self, request, queryset):
        # 移入移除回收站
        if queryset.filter(is_del=True):
            queryset.update(is_del=False)
        else:
            queryset.update(is_del=True)
    
    mark_delete.short_description = "移到回收站"
    

class CustomColumns:
    """ 自定义列表字段 """
    def operate(self, obj):
        # 自定义操作方法
        return format_html(
            '<a class="button1" href="{}">编辑</a> | <a class="deletelink1" href="{}">删除</a>',
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=(
                obj.pk, )),
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=(
                obj.pk, )),
        )

    operate.short_description = '操作'