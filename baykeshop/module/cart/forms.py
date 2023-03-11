from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from baykeshop.models import BaykeShopingCart

class BaykeShopingCartForm(ModelForm):
    
    class Meta:
        model = BaykeShopingCart
        fields = ['sku', 'num']
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }