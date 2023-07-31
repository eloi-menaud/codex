from typing import List, Optional
import re
from config import config

# ALL TREATMENT
def mdX(page):
    page = code_bloc(page)
    page = single_code_bloc(page)
    page = image(page)
    page = big_warnings(page)
    page = warnings(page)
    page = big_info(page)
    page = info(page)
    page = hr(page)
    page = small_hr(page)
    return page


def hr(page:str):
    pattern = r"---\n"
    replacement = r"<hr>\n"
    return re.sub(pattern, replacement, page)

def small_hr(page:str):
    pattern = r"-\n"
    replacement = r"<hr class='small'>\n"
    return re.sub(pattern, replacement, page,flags=re.DOTALL)


# custom markdown syntaxt : !- ... -! => warning block
def warnings(page:str):
    pattern = r"!-(.*?)-!"
    replacement = r"<span class='warn'>⚠️  \1</span>\n"
    return re.sub(pattern, replacement, page,flags=re.DOTALL)
def big_warnings(page:str):
    pattern = r"!!-(.*?)-!!"
    replacement = r"<div class='warn'>⚠️  \1</div>\n"
    return re.sub(pattern, replacement, page,flags=re.DOTALL)


# custom markdown syntaxt : n- ... -n => note block
def info(page:str):
    pattern = r"i-(.*?)-i"
    replacement = r"<span class='info'>ℹ️  \1</span>\n"
    return re.sub(pattern, replacement, page)
def big_info(page:str):
    pattern = r"ii-(.*?)-ii"
    replacement = r"<div class='info'>ℹ️  \1</div>\n"
    return re.sub(pattern, replacement, page,flags=re.DOTALL)




def image(page):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    replacement = fr"<div class='img-cont'><img src='../../../rsc/img/\2'><p>\1<p></div>\n"
    return re.sub(pattern, replacement, page)




# tag must be like "body" not "<body>"
def warp(src:str,tag:str):
    return f"<{tag}>\n{src}\n</{tag}>"



def single_code_bloc(page):
    pattern = r"`\s*([\s\S]+?)`"
    replacement = r"<span class='one'>\1</span>\n"
    return re.sub(pattern, replacement, page)







##--------- Syntaxe hightlight
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from pygments.token import Token, Comment, Keyword, Name, String, Number, Operator, Punctuation, Text



class CustomStyle(Style):
    styles = {
        Token:                  'bg:#1d1d1d',
        Comment:                '#717171',
        Keyword:                '#a98df3',
        Name.Tag:               '#a98df3',
        Name:                   '#ffffff',
        Name.Class:             '#f7ccb2',
        Name.Function:          '#69bcf9',
        String:                 '#6fcd90',
        Operator:               '#d99fce',
        Punctuation:            '#929292',
        Number:                 '#ea5b91'
    }
# creating .css associated -> rsc/pygments.css
with open('rsc/pygments.css','w') as f:
    f.write(HtmlFormatter(style=CustomStyle).get_style_defs('.highlight'))
#a19eff

def code_bloc(page):
    pattern = r"```([a-zA-Z]*)\s*([\s\S]+?)\s```"
    res = re.findall(pattern,page)
    for r in res:
        highlighted = ""
        if r[0] != '':
            langage, code = r
            highlighted = highlight(code, get_lexer_by_name(langage), HtmlFormatter(linenos=True))
        else :
            highlighted = highlight(r[1], get_lexer_by_name('text'), HtmlFormatter(linenos=True))
        page = re.sub(pattern, highlighted, page,count=1)

    return page


