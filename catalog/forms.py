from django import forms
from django.core.exceptions import ValidationError
from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар',
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field, forms.ImageField):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'

    def _check_forbidden_words(self, text):
        if not text:
            return
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word.lower() in text_lower:
                raise ValidationError(f'Поле содержит запрещенное слово: "{word}"')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        self._check_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        self._check_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            allowed_formats = ['image/jpeg', 'image/png']
            if image.content_type not in allowed_formats:
                raise ValidationError('Допустимые форматы изображения: JPEG и PNG.')
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError('Размер изображения не должен превышать 5 МБ.')
        return image
