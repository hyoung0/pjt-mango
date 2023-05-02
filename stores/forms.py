from django import forms
from .models import Store, StoreImage


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        exclude = ('like_users', 'latitude', 'longitude', )
        
        labels = {
            'name': '가게 이름',
            'phone_number': '전화번호',
            'info': '가게 정보',
            'address': '주소',
            'open_hours': '개장 시간',
            'closing_hours': '폐장 시간',
            'thumbnail': '썸네일 사진',
        }
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'phone_number': forms.TextInput(
                attrs={
                    'type': 'tel', 
                    'pattern': '[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}',
                    'class': 'form-control w-50',
                    }),
            'info': forms.Textarea(attrs={'class': 'form-control w-75', 'rows': '5'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'open_hours': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control w-25'}),
            'closing_hours': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control w-25'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control w-75'}),
        }


class StoreImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='가게 이미지 업로드',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
                'multiple': True,
            },
        ),
        required = False,
    )
    class Meta:
        model = StoreImage
        fields = ('image',)