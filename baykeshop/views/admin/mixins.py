from django.views.generic import CreateView
from baykeshop.models import BaykeMenu


class CreateMixins(CreateView):
    
    model = BaykeMenu
    context_object_name = f"{model}".lower()