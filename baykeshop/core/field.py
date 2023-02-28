from django.db.models import TextField


class HTMLField(TextField):
    
    def formfield(self, **kwargs):
        return super().formfield(**kwargs)