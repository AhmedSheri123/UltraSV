from store.models import Services
from modeltranslation.forms import TranslationModelForm
from django import forms
from accounts.models import UserProfile
from django.contrib.auth.models import User


class AddNewServiceForMeForm(forms.Form):
    content_ar = forms.CharField(widget=forms.Textarea, label="محتوى قصير عن الخدمة", required=False)
    content_en = forms.CharField(widget=forms.Textarea, label="محتوى قصير عن الخدمة", required=False)

class UserProfileForm(forms.ModelForm):
    sex = input
    class Meta:
        model = UserProfile
        fields = ['sex', 'address', 'address2', 'city', 'state', 'zip_code', 'countrys', 'phone_number']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'address2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'countrys': forms.Select(attrs={'class': 'form-control', 'style':"padding-right: 30px;"}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }