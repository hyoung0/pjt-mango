from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
       
        labels = {
            'username': '사용자 id',
            'address': '주소'
        },

        fields = (
            'username', 'password1', 'password2', 'nickname', 'email', 'address',
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2', 'email', 'address',]:
            self.fields[fieldname].help_text = None

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()

        labels = {
            'username': '사용자 id',
            'address': '주소',
            'image': '이미지',
        }

        # widgets = {
        #     'nickname': forms.CharField(attrs={'class': 'mx-auto'}),
        # }
        fields = (
            'nickname',
            'email',
            'image',
            'address'
        )

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

        for fieldname in ['nickname', 'email', 'image','address',]:
            self.fields[fieldname].help_text = None