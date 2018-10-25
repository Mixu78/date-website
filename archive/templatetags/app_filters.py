from math import floor

from django import template


register = template.Library()


@register.filter(name='divide')
def divide(value, arg):
    try:
        result = int(value) / int(arg)
        return int(result)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter(name="arrangePictures")
def arrangepictures(value, arg):
    try:
        columnsize = divide(arg+3, 4)  # args + 4 to ensure not 5 columns are created.
        print(columnsize)
        return bool(value % columnsize) is False
    except (ValueError, ZeroDivisionError):
        return None
