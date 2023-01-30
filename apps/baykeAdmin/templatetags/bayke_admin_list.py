import json
from django.template import Library
from django.contrib.admin.templatetags.admin_list import results
from django.utils.safestring import mark_safe

register = Library()



            

@register.simple_tag
def result_list(cl):
    # print(list(results(cl)))
    # print(cl.__dict__)
    
    list_display = cl.list_display
    qs = cl.result_list.values(*[i for i in list_display if i != 'action_checkbox'])
    # return json.dumps(list(qs), ensure_ascii=False)
    return list(qs)

        

    
    