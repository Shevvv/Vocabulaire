from django.core.management.base import BaseCommand
from Vocabulaire.models import RussianWord, DutchWord, PartOfSpeech
from django.db.utils import IntegrityError


class Command(BaseCommand):

    help = "Update database entries from the new_words.txt source file"

    def add_arguments(self, parser):
        parser.add_argument("filename", nargs=1, type=str)

    def handle(self, *args, **options):
        with open(f"{options['filename'][0]}.txt", encoding='utf-8') as f:
            data = f.read().rstrip()

        for line in data.split('\n'):
            russian_str, dutchs_str = line.split(' = ')
            russian, russian_pos_str = str_to_lexeme(russian_str)

            russian_word = retrieve_word(russian, RussianWord)
            russian_pos = retrieve_pos(russian_pos_str)
            russian_word.part_of_speech.add(russian_pos)

            for dutch_str in dutchs_str.split(', '):
                dutch, dutch_pos_str = str_to_lexeme(dutch_str)
                dutch_word = retrieve_word(dutch, DutchWord)
                dutch_pos = retrieve_pos(dutch_pos_str)
                dutch_word.part_of_speech.add(dutch_pos)
                dutch_word.translations.add(russian_word)
                dutch_word.save()
                print(f"{dutch_word} has been successfully saved as "
                      f"translation to {russian_word}")
            russian_word.save()


def str_to_lexeme(string):
    string_lst = string.split(' ')
    return ' '.join(string_lst[:-1]), string_lst[-1][1:-1]


def retrieve_word(word_str: str, model):
    try:
        word = model(lexeme=word_str)
        word.save()
    except IntegrityError:
        word = model.objects.get(lexeme=word_str)
        print(f"{model._meta.verbose_name.title()} '{word_str}' already "
              f"exists. Retrieving from database")
    else:
        print(f"{model._meta.verbose_name.title()}' {word_str}' created "
              f"successfully")
    return word


def retrieve_pos(pos_str: str):
    try:
        return PartOfSpeech.objects.get(abbr=pos_str)
    except PartOfSpeech.DoesNotExist:
        raise ValueError(f"{pos_str} is not a defined part of "
                         f"speech")
