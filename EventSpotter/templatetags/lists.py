from django import template

register = template.Library()


@register.filter
def index(list_given, i):
    return list_given[i]


register.filter("index", index)


@register.filter
def size(list_given):
    return len(list_given)


register.filter("size", size)
