from baykeshop.module.payment.alipay import AliPay, AliPayConfig
from baykeshop.config.settings import bayke_settings

# private_key_string
with open(bayke_settings.ALIPAY_PRIVATE_KEY, 'r') as f:
    private_key_string = f.read()

# public_key_string
with open(bayke_settings.ALIPAY_PUBLIC_KEY, 'r') as f:
    public_key_string = f.read()


alipay = AliPay(
    appid=bayke_settings.ALIPAY_APPID,
    app_notify_url=None,  # 默认回调 url
    app_private_key_string=private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=public_key_string,
    sign_type=bayke_settings.ALIPAY_SIGN_TYPE,  # RSA 或者 RSA2
    debug=bayke_settings.ALIPAY_DEBUG,  # 默认 False
    verbose=bayke_settings.ALIPAY_DEBUG,  # 输出调试数据
    config=AliPayConfig(timeout=bayke_settings.ALIPAY_TIMOUT)  # 可选，请求超时时间
)