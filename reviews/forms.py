from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label='리뷰 내용',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    CHOICES = [
        (1, 1), 
        (2, 2), 
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    rating = forms.ChoiceField(
        label='평점',
        widget=forms.TextInput(
            attrs={
                'class': 'form-select',
            }
        ),
        choices=CHOICES,
    )
    image = forms.ImageField(
        label='사진 업로드',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    class Meta:
        model = Review
        fields = ('content', 'rating', 'image',)