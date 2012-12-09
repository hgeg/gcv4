from django import template

register = template.Library()

@register.filter
def percent(value,arg):
    return int(((value*1.0)/arg)*100)