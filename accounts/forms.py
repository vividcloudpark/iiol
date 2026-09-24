from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .regions import region_choices


class SignupForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    region_code = forms.ChoiceField(label="내 지역", choices=region_choices())

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "region_code")
        labels = {"username": "아이디", "first_name": "이름", "last_name": "성"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email


class ProfileForm(forms.ModelForm):
    region_code = forms.ChoiceField(label="내 지역", choices=region_choices())

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "region_code")
        labels = {"email": "이메일", "first_name": "이름", "last_name": "성"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email).exists():
            raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email
