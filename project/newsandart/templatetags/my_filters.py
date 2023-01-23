from django import template


register = template.Library()

@register.filter()
def censor(value):
    forbiddens = ['тыгын', 'кино', 'родина']

    if not isinstance(value, str):
        raise TypeError(f"Недопустимое значение '{type(value)}'Нужно ввести строковое значение")

    for word in value.split():
        if word.lower() in forbiddens:
            value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return value



