from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter,CharFilter
from django.forms import DateTimeInput
from .models import Category

class PostFilter(FilterSet):

    title = CharFilter(field_name="title", label='Заголовок', lookup_expr="icontains")
    postCategory = ModelChoiceFilter(field_name="postCategory", queryset=Category.objects.all(), label='Категория', lookup_expr="exact", empty_label="Выберите")
    datecalbefore = DateTimeFilter(field_name="dateCreation", lookup_expr="lt",
                                  label='Дата публикации до:',
                                  widget=DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                       attrs={"type": "datetime-local"}, ), )
    datecalafter = DateTimeFilter(field_name="dateCreation", lookup_expr="gt",
                                  label='Дата публикации после:',
                                  widget=DateTimeInput(format="%Y-%m-%dT%H:%M",
                                                       attrs={"type": "datetime-local"}, ), )

