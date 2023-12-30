from django.shortcuts import render
from django.urls import reverse
from django.db.models.functions import Lower
from .models import DutchWord, RussianWord
import json


def index(request):
    return render(request, "Vocabulaire/index.html")


def dutch(request):
    lexemes = DutchWord.objects.order_by(Lower('lexeme'))
    subtitle = "Nederlands naar Russisch"
    link = 'dutch_word'
    url_link = reverse(dutch_word, args=["$"])
    breadcrumb = ['dutch']
    qs_json = json.dumps(list(DutchWord.objects.order_by(Lower('lexeme')).
                              values()))
    context = {
        'lexemes': lexemes,
        'subtitle': subtitle,
        'link': link,
        'url_link': url_link,
        'breadcrumb': breadcrumb,
        'qs_json': qs_json,
    }
    return render(request, "Vocabulaire/entries.html", context)


def russian(request):
    lexemes = sorted(RussianWord.objects.all(),
                     key=lambda x: x.lexeme.lower())
    subtitle = "Russisch naar Nederlands"
    link = 'russian_word'
    url_link = reverse(russian_word, args=["$"])
    breadcrumb = ['russian']
    qs_json = json.dumps(sorted(list(RussianWord.objects.values()),
                                key=lambda x: x['lexeme'].lower()))
    context = {
        'lexemes': lexemes,
        'subtitle': subtitle,
        'link': link,
        'url_link': url_link,
        'breadcrumb': breadcrumb,
        'qs_json': qs_json,
    }
    return render(request, "Vocabulaire/entries.html", context)


def russian_word(request, word_lexeme):
    word = RussianWord.objects.get(lexeme=word_lexeme)
    t_link = 'dutch_word'
    breadcrumb = ['russian', str(word)]
    translations = word.dutchword_set.all()
    context = {'word': word,
               'translations': translations,
               't_link': t_link,
               'breadcrumb': breadcrumb}
    return render(request, "Vocabulaire/word.html", context)


def dutch_word(request, word_lexeme):
    word = DutchWord.objects.get(lexeme=word_lexeme)
    t_link = 'russian_word'
    breadcrumb = ['dutch', str(word)]
    translations = word.translations.all()
    context = {'word': word,
               'translations': translations,
               't_link': t_link,
               'breadcrumb': breadcrumb}
    return render(request, "Vocabulaire/word.html", context)
