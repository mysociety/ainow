from django import template

register = template.Library()

@register.filter
def organisers_by_schedule(item, schedule):
    return item.filter(organiserscheduletype__schedule=schedule)
