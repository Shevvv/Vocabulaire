from django.contrib import admin

from Vocabulaire.models import DutchWord, RussianWord, PartOfSpeech, \
    Homework, Task

admin.site.register(PartOfSpeech)
admin.site.register(DutchWord)
admin.site.register(RussianWord)
admin.site.register(Homework)
admin.site.register(Task)
