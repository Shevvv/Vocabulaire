from django.db import models
from ckeditor.fields import RichTextField


class PartOfSpeech(models.Model):
    name = models.CharField(max_length=200, unique=True)
    abbr = models.CharField(max_length=15, unique=True)

    class Meta:
        verbose_name_plural = 'parts of speech'

    def __str__(self):
        return self.name


class RussianWord(models.Model):
    lexeme = models.CharField(max_length=200, unique=True)
    part_of_speech = models.ManyToManyField(to=PartOfSpeech)

    def __str__(self):
        return self.lexeme


class DutchWord(models.Model):
    lexeme = models.CharField(max_length=200, unique=True)
    translations = models.ManyToManyField(to=RussianWord)
    part_of_speech = models.ManyToManyField(to=PartOfSpeech)

    def __str__(self):
        return self.lexeme


class Homework(models.Model):
    created = models.DateTimeField(null=True)
    deadline = models.DateField()
    topic = models.CharField(max_length=200)
    done = models.BooleanField()

    def __str__(self):
        return self.topic


class Task(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    description = models.TextField()
    content = RichTextField()

    def __str__(self):
        return str(self.homework) + ". Opdracht #" + \
               str(list(self.homework.task_set.all()).index(self) + 1)


class Update(models.Model):
    created = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=200)
    text = RichTextField()

    def __str__(self):
        return str(self.created)
