from django.forms import ModelForm
from .models import Blog


class BlogModelForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','body']
