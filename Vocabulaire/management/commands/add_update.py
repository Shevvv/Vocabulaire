from django.core.management.base import BaseCommand
from Vocabulaire.models import Homework, Update
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from string import ascii_uppercase as au, ascii_lowercase as al


class Command(BaseCommand):

    help = "Update database entries from the new_words.txt source file"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1, type=str)

    def handle(self, *args, **options):
        data = read_file(options['filename'][0])
        if data['type'] == 'homework':
            try:
                homework = Homework.objects.get(id=data['id'])
            except KeyError:
                raise KeyError("the source file must specify homework ID")
            else:
                update = Update(name=data['name'],
                                text=process_text(data['text'], homework,
                                                  data['type']))
                update.save()
                homework.created = timezone.make_aware(datetime.now(),
                                   timezone.get_current_timezone())
                homework.save()


def read_file(filename):
    with open(filename + '.txt') as f:
        data = f.read().rstrip()

    return {line.split(': ')[0]: line.split(': ')[1]
            for line in data.split('\n')}


def process_text(text, db_object, mode):
    p = 0
    new_text = ''
    a = None
    match mode:
        case 'homework':
            view = 'tasks'
        case _:
            raise ValueError(f"incorrect mode '{mode}'")
    while p < len(text):
        if text[p] == '%':
            a = p
        elif a is not None and not (text[p] in au or text[p] in al):
            new_text = text[:a]
            keyword = text[a+1:p]
            text = text[p:]
            match keyword:
                case 'TOPIC':
                    insert = db_object.topic
                case 'LINK':
                    insert = f'<a href={reverse(view, args=[db_object.id])}>' \
                             f'{db_object.topic}</a>'
                case _:
                    raise ValueError(f"Unrecognized keyword '{keyword}'")
            new_text += insert
            p = 1
            a = None
            continue
        p += 1
    return new_text + text
