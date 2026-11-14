from django.contrib.auth.forms import UserCreationForm
from users.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs.update({'class': 'form-control border border-primary', })
        self.fields['username'].widget.attrs.update({'class': 'form-control border border-primary', })

    error_messages = {
        'invalid_login': _('Неверный логин или пароль.'),
        'inactive': _('Этот аккаунт заблокирован. Обратитесь к администратору или менеджеру.'),
    }

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')
        return super().confirm_login_allowed(user)


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].help_text = None
        self.fields['password2'].label = 'Повторите пароль'
        self.fields['password2'].help_text = None

        for fild in ['email', 'password1', 'password2', 'avatar', 'phone_number', 'country']:
            self.fields[fild].widget.attrs.update({'class': 'form-control border border-primary', })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2', 'avatar', 'phone_number', 'country')
