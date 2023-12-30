from django.db import models


class RussianWord(models.Model):
    lexeme = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.lexeme


class DutchWord(models.Model):
    lexeme = models.CharField(max_length=200, unique=True)
    translations = models.ManyToManyField(to=RussianWord)

    def __str__(self):
        return self.lexeme
