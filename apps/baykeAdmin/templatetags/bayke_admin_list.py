import json
from django.template import Library
from django.contrib.admin.templatetags.admin_list import (
    results, result_headers, _coerce_field_name
)
from django.utils.safestring import mark_safe
from django.contrib.admin.utils import (
    display_for_field,
    display_for_value,
    get_fields_from_path,
    label_for_field,
    lookup_field,
)

register = Library()


def _list_display(list_display):
    return [i for i in list_display if i != 'action_checkbox']

def show_result_headers(cl):
    # print(cl.__dict__)
    # print(cl.search_fields)
    # print(cl.list_editable)
    headers = []
    ordering_field_columns = cl.get_ordering_field_columns()
    for i, field_name in enumerate(_list_display(cl.list_display)):
        column_dict = {}
        text, attr = label_for_field(
            field_name, cl.model, model_admin=cl.model_admin, return_attr=True
        )
        is_field_sortable = cl.sortable_by is None or field_name in cl.sortable_by
        is_field_search = cl.search_fields is None or field_name in cl.search_fields
        
        column_dict['field'] = field_name
        column_dict['label'] = text
        column_dict['sortable'] = is_field_sortable
        column_dict['searchable'] = is_field_search
        headers.append(column_dict)
        # print(attr)
    return headers


@register.inclusion_tag('baykeAdmin/change/change_results_list.html')
def show_results(cl):
    list_display = cl.list_display
    qs = cl.result_list.values(*[i for i in list_display if i != 'action_checkbox'])
    headers = show_result_headers(cl)
    return {
        'changeListData': list(qs),
        'headerData': headers,
        'total': cl.full_result_count,
        'per_page': cl.list_per_page,
        'currentPage': cl.page_num
    }

    
    