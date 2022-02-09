from django import template
register = template.Library()
from django.conf import settings
from Market.const import server_list
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

@register.filter
def stringFormat(string):
    return string.replace('{img green_up_arrow 16 16}','▲' ) \
                 .replace('{img green_down_arrow 16 16}', '▼')

@register.filter
def stringFormat(string):
    return string.replace('{img green_up_arrow 16 16}','▲' ) \
                 .replace('{img green_down_arrow 16 16}', '▼')
@register.filter
def getMaxSFR(skill):
    try:
        return skill.sfr[skill.max_lv]
    except:
        return 0

@register.filter
def cdtosec(cd):
    return '%ss' % (cd/1000 )


@register.filter
def parseEffect(effect, obj):
    specialvar= {
        '#{CaptionRatio}#'  : 'captionratio1', 
        '#{CaptionRatio2}#' : 'captionratio2', 
        '#{CaptionRatio3}#' : 'captionratio3',
        '#{SkillSR}#'       : 'skillsr', 
        '#{SpendItemCount}#': 'spenditemcount' , 
        '#{SkillFactor}#'   : 'sfr',
        '#{CaptionTime}#'   : 'captiontime',
        '#{SpendItemCount}#': 'spenditemcount', 
        '#{SpendPoison}#'   : 'spendpoison',   
        '#{SpendSP}#'       : 'spendsp'
    }
    effect = effect.replace('{#339999}{ol}','').split('{nl}')
    ef = []
    for lines in effect:
        lines = lines.replace('{','').replace('}','').replace('//','').split('#')
        # new_lines = []
        # for word in lines:
        #     if word in specialvar:
        #         if (obj[specialvar[word]] == None):
        #             continue
        #         word = obj[specialvar[word]][0]
        #     new_lines.append(word)
        ef.append(lines)
    return ef


def parseEffect(effect):
    
    effect = effect.replace('{#339999}{ol}','').split('{nl}')
    ef = []
    for lines in effect:
        lines = lines.replace('{','').replace('}','').replace('//','').split('#')
        ef.append(lines)
    return ef

@register.filter
def parseBonus(bonus):
    return bonus.replace('{img green_up_arrow 16 16}', '▲')\
                                .replace('{img green_down_arrow 16 16}', '▼').replace('{nl}' , '<br>')
    return bonus_all

@register.filter
def splitnl(string):
    return ('<br>').join(string.split('{nl}'))

@register.filter 
def intspace(ints):
    return '{:,}'.format(ints).replace(',', ' ')

@register.filter
def translateServer(string):
    try:
        return server_list[settings.REGION][str(string)]
    except:
        return string
