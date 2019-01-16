from django import forms
from lab_app.models import Review, Film
from django.contrib.auth.models import User


# Форма регистрации
class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'awaiting'}
            ),
        }


# Форма авторизации
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'awaiting'}
            ),
        }


# Форма добавления
class AddFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'awaiting'}
            ),
        }


# Форма создания отзыва
class PostReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'awaiting'}
            ),
        }

# Форма изменения


class ChangeForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def clean_name(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()

        return user