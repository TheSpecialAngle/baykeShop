from django.forms.widgets import TextInput


class SearchTextInput(TextInput):
    
    input_type = "search"
    template_name = "baykeShop/widgets/search_form.html"