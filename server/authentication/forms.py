from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 5:
            raise forms.ValidationError('Пароль короче 5 символов')

        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Пароль должен содержать минимум одну заглавную букву')

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Пароль должен содержать минимум одну цифру')

        return password

    def save(self, commit=True):
        return get_user_model().objects.create_user(**self.cleaned_data)


class LoginForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['password']
