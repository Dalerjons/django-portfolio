from django import template
from cinema.models import Category


register = template.Library()  # Декорател для функций


# Функция которая будит возвращать все категории
@register.simple_tag()  # Декротором сказали что функ можно вызывать в любом html файле
def get_categories():
    return Category.objects.all()






