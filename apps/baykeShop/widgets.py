from django.forms.widgets import TextInput as BaseTextInput


class SearchTextInput(BaseTextInput):
    
    input_type = "search"
    template_name = "baykeShop/widgets/input.html"
    

class TextInput(BaseTextInput):
    
    input_type = "text"
    template_name = "baykeShop/widgets/input.html"


class PasswordInput(BaseTextInput):
    
    input_type = "password"
    template_name = "baykeShop/widgets/input.html"