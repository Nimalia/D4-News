from django import forms
# from django.core.exceptions import ValidationError
from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    # author = forms.ModelChoiceField(label='Автор', queryset=Author.objects.all())
    title = forms.CharField(label='Заголовок')
    categoryType = forms.ChoiceField(label='Тип', choices=Post.CATEGORY_CHOICE)
    text = forms.CharField(widget=forms.Textarea, label='Текст')
    postCategory = forms.ModelMultipleChoiceField(label='Категория', queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'categoryType', 'text', "postCategory",]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     Post.text = cleaned_data.get("text")
    #     Post.title = cleaned_data.get("title")
    #
    #     if Post.title == Post.text:
    #         raise ValidationError(
    #             "Описание не должно быть идентично названию."
    #         )
    #
    #     return cleaned_data



