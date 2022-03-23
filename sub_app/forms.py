from django import forms
from .models import SignModel

class SignForm(forms.ModelForm):
	class Meta:
		model=SignModel
		fields = "__all__"