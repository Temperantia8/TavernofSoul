from django import template
register = template.Library()
from django.conf import settings
import re

@register.filter
def access(value, value2):
	try:
		return value['data'][value2]
	except:
		return ""
@register.filter
def hasChange(row, col):
	return row['data'][col] == row['data_old'][col]


@register.filter
def imcFormatRemover(string):
    string = string.split('{nl}')
    s2 = []
    for i in string:
        s2.append( re.sub(r'\{(.*?)\}', '', i) )
    return s2[0]