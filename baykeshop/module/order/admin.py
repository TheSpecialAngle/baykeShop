from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.contrib import messages
from django.utils.translation import ngettext


from baykeshop.public.admin import BaseModelAdmin
from baykeshop.public.sites import bayke_site
from baykeshop.models import (
    BaykeShopOrderInfo, BaykeShopOrderSKU
)

ORDER_SKUS_STRING = """
    <div class='orderSKU'>
        <div><img src='{}' /></div>
        <div>
            <p>{}</p>
            <span class='spec'>规格：{}</span>
        </div>
    </div>
"""

@admin.register(BaykeShopOrderInfo, site=bayke_site)
class BaykeShopOrderInfoModelAdmin(BaseModelAdmin):
    
    list_display = (
        'id', 
        'order_sn',
        'dis_owner',
        'dis_order_sku',
        'pay_status', 
        'dis_pay_method', 
        'total_amount', 
        'dis_order_mark',
        'pay_time',
        'operate'
    )
    # list_editable = ('pay_status', )
    search_fields = ('owner__username', 'order_sn',)
    search_help_text = "支持通过用户名和订单号搜索"
    # list_editable = ('total_amount', )
    list_filter = ('pay_status', 'pay_method')
    list_display_links = ('order_sn',)
    list_select_related = ('owner',)
    readonly_fields = ('pay_status', 'dis_order_sku',)
    actions = ['dis_acticon_order']
    
    @admin.display(description="用户")
    def dis_owner(self, obj):
        return obj.owner.username
        
    @admin.display(description="订单备注")
    def dis_order_mark(self, obj):
        return obj.order_mark[:15]
        
    @admin.display(description="支付方式")
    def dis_pay_method(self, obj):
        if obj.pay_method == 4:
            return format_html(
                "<span style='color:red'>{}</span>", 
                obj.get_pay_method_display()
            )
        elif obj.pay_method == 2:
            return format_html(
                "<span style='color:blue;'>{}</span>", 
                obj.get_pay_method_display()
            )
        elif obj.pay_method == 3:
            return format_html(
                "<span style='color:green'>{}</span>", 
                obj.get_pay_method_display()
            )
        return obj.get_pay_method_display()
    
    @admin.display(description="订单商品")
    def dis_order_sku(self, obj):
        order_skus = obj.baykeshopordersku_set.all()
        order_skus_html = format_html_join('\n', ORDER_SKUS_STRING, 
            ((u.sku.cover_pic.url, u.title, u.spec) for u in order_skus)
        )
        return order_skus_html
    
    @admin.action(permissions=['change'], description="对选中订单，一键发货")
    def dis_acticon_order(self, request, queryset):
        updated = queryset.filter(pay_status=2).update(pay_status=3)
        self.message_user(request, ngettext(
            '%d 商品支付状态已成功标记为待收货.',
            '%d 商品支付状态已成功标记为待收货.',
            updated,
        ) % updated, messages.SUCCESS)
    
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=None) -> bool:
        # 订单处于待支付状态允许修改，其他状态不允许修改
        if obj is not None and obj.pay_status != 1:
            return False
        return super().has_change_permission(request, obj)
    class Media:
        css = {'all': ['baykeadmin/css/ordersku.css']}
        