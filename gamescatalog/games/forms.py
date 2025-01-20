from django.forms.widgets import DateInput, ClearableFileInput, URLInput, SelectMultiple, Select

from .models import *
from django.forms import ModelForm, TextInput, Textarea
from django import forms

class GamesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Оберіть категорію"

    class Meta:
        model = Games
        fields = ['title', 'developer',
                  'date', 'description', 'image',
                  'trailer_url', 'platforms', 'cat']

        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва гри',
            }),
            'developer': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Розробник',
            }),
            'date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата релізу'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опис гри'
            }),
            'image': ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'trailer_url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Посилання на трейлер'
            }),
            'platforms': SelectMultiple(attrs={
                'class': 'form-select',
            }),
            'cat': Select(attrs={
                'class': 'form-select',
            })
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Довжина більша за 200!')
        return title


class GameFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        required=False,
        label=False,
        empty_label="Категорія",
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            "class": "form-control"
        })
    )
    platform = forms.ModelChoiceField(
        queryset=Platforms.objects.all(),
        required=False,
        label=False,
        empty_label="Платформа",
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            "class": "form-control"
        })
    )
    date = forms.ChoiceField(
        choices=[
            ('', 'Дата релізу'),
            ('last_month', 'За минулий місяць'),
            ('last_year', 'За минулий рік')
        ],
        required=False,
        label=False,
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            "class": "form-control"
        })
    )
    search = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={
            "onchange": "this.form.submit()",
            "class": "form-control",
            "placeholder": "Пошук..."
        })
    )