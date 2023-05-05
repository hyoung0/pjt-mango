from django import forms
from .models import Store, StoreImage, Menu
from taggit.managers import TaggableManager
from taggit.forms import TagField, TagWidget
from django.forms import inlineformset_factory

class StoreForm(forms.ModelForm):
    category = forms.ChoiceField(
        label='카테고리',
        widget=forms.Select(
            attrs={
                'placeholder': '카테고리 입력',
                'class': 'form-select',
            }
        ),
        choices = (('퓨전 중식','퓨전 중식'), ('전통 중식', '전통 중식'), 
        ('퓨전 한식','퓨전 한식'), ('전통 한식','전통 한식'),
        ('닭 오리 요리', '닭 오리 요리'), ('카페 디저트', '카페 디저트'), 
        ('고기 요리', '고기 요리'), ('해산물', '해산물'), 
        ('이탈리안', '이탈리안'), ('프랑스 음식', '프랑스 음식'), 
        ('국수 면 요리', '국수 면 요리'), ('퓨전 양식', '퓨전 양식'), 
        ('분식', '분식'), ('탕 찌개 전골', '탕 찌개 전골'),
        ('브런치 버거 샌드', '브런치 버거 샌드'), ('일식', '일식'),
        ('기타 양식', '기타 양식'), ('패스트 푸드', '패스트 푸드'),
        ('돼지 고기', '돼지 고기'), ('소고기', '소고기')
        ), 
        required=True,
    )

    class Meta:
        model = Store
        exclude = ('like_users', 'latitude', 'longitude', 'hits')
        
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
            'name': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'phone_number': forms.TextInput(
                attrs={
                    'type': 'tel', 
                    'pattern': '[0-9]{2,3}-[0-9]{3,4}-[0-9]{4}',
                    'class': 'form-control w-75',
                    }),
            'info': forms.Textarea(attrs={'class': 'form-control w-75', 'rows': '5'}),
            'address': forms.TextInput(attrs={'class': 'form-control w-75'}),
            'open_hours': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control w-50'}),
            'closing_hours': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control w-50'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': "콤마 구분"}),
        }


class StoreImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='가게 이미지 업로드',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control mb-5',
                'multiple': True,
            },
        ),
        required = False,
    )
    class Meta:
        model = StoreImage
        fields = ('image',)


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('menu', 'price',)
        labels = {
            'menu': '메뉴 이름',
            'price': '가격',
        }
        widgets={
            'menu': forms.TextInput(attrs={'class':'form-control',}),
            'price': forms.NumberInput(attrs={'class':'form-control',}),
        }

MenuFormSet = inlineformset_factory(Store, Menu, form=MenuForm, extra=4, can_delete=False)