from django.conf import settings

BAYKE_DEFAULTS = {
    
    # LOGO
    "LOGO_URL": "/static/baykeshop/img/logo.png",
    
    # 搜索框默认搜索词
    "SEARCH_VALUE": "请输入搜索词...",
    
    # 手机号验证正则
    "PHONE_REGX": r"^1[35678]\d{9}$",
    
    # PC商城登陆成功后跳转地址
    "NEXT_PAGE": "baykeshop:home",
    
    # 首页楼层显示商品数量
    "HOME_GOODS_COUNT": 10,
    
    # 商品列表页每页显示个数
    "GOODS_PAGINATE_BY": 24,
    
    # 商品列表页最后一页剩余几个
    # 自动添加到上一页的个数，该值必须小于分页值
    "GOODS_PAGINATE_ORPHANS": 4,
    
    # 商品详情页评论每页显示数量
    "DETAIL_COMMENTS_PAGINATE_BY": 24,
    
    # 管理后台是否启用自定义菜单
    "ADMIN_MENUS": True,
    
    # 后台logo文字
    "SITE_HEADER": "BaykeShop后台管理",
    
    # 后台title后缀
    "SITE_TITLE": "BaykeShop商城系统",
    
    # 支付宝相关配置
    "ALIPAY_PRIVATE_KEY": settings.BASE_DIR / "baykeshop/pay/alipay/keys/app_private_key.pem",
    "ALIPAY_PUBLIC_KEY": settings.BASE_DIR / "baykeshop/pay/alipay/keys/app_public_key.pem",
    "ALIPAY_APPID": "2021000116697536",
    "ALIPAY_NOTIFY_URL": "baykeshop:alipay_notify",
    "ALIPAY_RETURN_URL": "baykeshop:alipay_notify",
    "ALIPAY_SIGN_TYPE": "RSA2",  # RSA 或者 RSA2
    "ALIPAY_DEBUG": settings.DEBUG,
    "ALIPAY_TIMOUT": 15
}