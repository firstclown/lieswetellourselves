from django import forms
from lieswetellourselves.lies.models import Lie

class LieForm(forms.ModelForm):
    class Meta:
        model = Lie
