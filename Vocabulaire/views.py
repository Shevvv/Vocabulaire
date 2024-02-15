from django.shortcuts import render
from django.urls import reverse
from django.db.models.functions import Lower
from .models import DutchWord, RussianWord, PartOfSpeech, Homework, Update
from urllib.parse import unquote
from datetime import datetime, date


def index(request):
    updates = Update.objects.order_by('created')
    context = {'hour': datetime.now().hour, 'breadcrumb': [],
               'breadcrumbs_names': [], 'updates': updates}
    return render(request, "Vocabulaire/index.html", context)


def dutch(request):
    lexemes = DutchWord.objects.order_by(Lower('lexeme'))
    lexemes = {str(lexeme): lexeme.translations.all() for lexeme in lexemes}
    parts_of_speech = PartOfSpeech.objects.order_by('name')
    subtitle = "Nederlands naar Russisch"
    link = 'dutch_word'
    t_link = 'russian_word'
    breadcrumb = ['dutch']
    breadcrumb_names = [unquote(page)
                        for page in reverse('dutch').strip("/").split("/")]
    context = {
        'lexemes': lexemes,
        'parts_of_speech': parts_of_speech,
        'subtitle': subtitle,
        'link': link,
        't_link': t_link,
        'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
    }
    return render(request, "Vocabulaire/entries.html", context)


def russian(request):
    lexemes = sorted(RussianWord.objects.all(),
                     key=lambda x: x.lexeme.lower())
    lexemes = {str(lexeme): lexeme.dutchword_set.all() for lexeme in lexemes}
    parts_of_speech = PartOfSpeech.objects.order_by('name')
    subtitle = "Russisch naar Nederlands"
    link = 'russian_word'
    t_link = 'dutch_word'
    breadcrumb = ['russian']
    breadcrumb_names = [unquote(page)
                        for page in reverse('russian').strip("/").split("/")]
    context = {
        'lexemes': lexemes,
        'parts_of_speech': parts_of_speech,
        'subtitle': subtitle,
        'link': link,
        't_link': t_link,
        'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
    }
    return render(request, "Vocabulaire/entries.html", context)


def russian_word(request, word_lexeme):
    word = RussianWord.objects.get(lexeme=word_lexeme)
    t_link = 'dutch_word'
    translations = word.dutchword_set.all()
    breadcrumb = ['russian', 'russian_word']
    breadcrumb_names = [unquote(page) for
                        page in reverse('russian_word',
                        args=[word_lexeme]).strip("/").split("/")]
    context = {'word': word,
               'translations': translations,
               't_link': t_link,
               'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
               }
    return render(request, "Vocabulaire/word.html", context)


def dutch_word(request, word_lexeme):
    word = DutchWord.objects.get(lexeme=word_lexeme)
    t_link = 'russian_word'
    breadcrumb = ['dutch', 'dutch_word']
    breadcrumb_names = [unquote(page) for page in reverse('dutch_word',
                    args=[word_lexeme]).strip("/").split("/")]
    translations = word.translations.all()
    context = {'word': word,
               'translations': translations,
               't_link': t_link,
               'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
               }
    return render(request, "Vocabulaire/word.html", context)


def homework(request):
    homeworks = Homework.objects.order_by('-deadline')
    today = date.today()
    breadcrumb = ['homework']
    breadcrumb_names = [unquote(page)
                        for page in reverse('homework').strip("/").split("/")]
    context = {
        'homeworks': homeworks,
        'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
        'today': today,
    }
    return render(request, "Vocabulaire/homework.html", context)


def tasks(request, homework_id):
    homework = Homework.objects.get(id=homework_id)
    tasks = homework.task_set.all()
    breadcrumb = ['homework', 'tasks']
    breadcrumb_names = [unquote(page) for page in reverse('tasks', args=[
        homework_id]).strip(
        "/").split("/")]
    breadcrumb_names[-1] = str(homework)
    today = date.today()
    context = {
        'breadcrumb': list(zip(breadcrumb, breadcrumb_names)),
        'homework': homework,
        'tasks': tasks,
        'today': today,
    }
    return render(request, "Vocabulaire/tasks.html", context)
