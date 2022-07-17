from django import forms
from .models import Ejecucion,Spider
class SpiderForm(forms.Form):
    spider = forms.ModelChoiceField(queryset=Spider.objects.all())

