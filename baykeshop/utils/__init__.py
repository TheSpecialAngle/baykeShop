import urllib.request
import urllib.parse

def stats_req(request):
    data = urllib.parse.urlencode({
        "url": request.get_host(),
        "scheme": request.scheme,
        "port": request.get_port(),
        "user_aget":request.META['HTTP_USER_AGENT'],
        "ip": (
                request.META.get('HTTP_X_FORWARDED_FOR') 
                if request.META.get('HTTP_X_FORWARDED_FOR') 
                else request.META['REMOTE_ADDR']
            ),
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url="http://www.bayke.shop/stats/", 
        method="POST", 
        data=data
    )
    
    with urllib.request.urlopen(req) as f:
        pass