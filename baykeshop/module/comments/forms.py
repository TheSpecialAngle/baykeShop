from django import forms

from baykeshop.models import BaykeOrderInfoComments


class BaykeOrderInfoCommentsModelForm(forms.ModelForm):
    
    class Meta:
        model = BaykeOrderInfoComments
        fields = ('content', 'comment_choices', 'object_id')
        widgets = {
            'content': forms.Textarea(attrs={"class":"textarea","rows": 5,  "placeholder":"请如实发表您对该商品的感受..."}),
        }
