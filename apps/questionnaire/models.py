from django.db import models
from accounts.models import Club, Player
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Questionnaire(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    club = models.ManyToManyField(Club, blank=True)

    def __str__(self):
        return self.name


class Section(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    heading = models.CharField(max_length=64)
    sort = models.IntegerField()

    def __str__(self):
        return self.heading + ' of ' + self.questionnaire.name


class Question(models.Model):
    text = models.TextField(blank=True, verbose_name=_("Text"))
    section = models.ForeignKey(Section)
    sort = models.IntegerField()
    slug = models.SlugField(max_length=100, unique=True)
    TYPE_CHOICES = (
        #('choice-yesno', _('Choice: Yes or No')),
        #('choice-yesnocomment', _('Choice & Comment: Yes or No with a chance to comment on the answer')),
        ('open', _('Open: A simple one line input box')),
        ('open-textfield', _('Textfield: A box for lengthy answers')),
        #('choice', _('Choice: A list of choices to choose from')),
        #('choice-freeform', _('Choice & Free Form: A list of choices with a chance to enter something else')),
        #('choice-multiple', _('Multiple Choice: A list of choices with multiple answers')),
        #('choice-multiple-freeform', _('Multiple Choice & Free Form: '
        #                               'Multiple Answers with multiple user defined answers')),
        ('range', _('Range: A range of options from which can be chosen')),
        ('number', _('Number: A number')),
        ('comment', _('Comment: Not a question, but only a comment displayed to the user')),
    )
    question_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    required = models.BooleanField(default=True, help_text="Is field required to answer?")
    input_placeholder = models.CharField(blank=True, null=True, max_length=200)
    extra = JSONField(blank=True, default=dict())
    footer = models.TextField(u"Footer", help_text="Footer rendered below the question interpreted as textile",
                              blank=True)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question)
    sort = models.IntegerField()
    value = models.CharField(u"Short Value", max_length=64)
    text = models.CharField(u"Choice Text", max_length=200)

    def __unicode__(self):
        return u'(%s) %d. %s' % (self.question.number, self.sortid, self.text)


class Submission(models.Model):
    player = models.ForeignKey(Player, help_text="The player who supplied this answer")
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' on '.join([self.player.user.username, str(self.date)])


class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, help_text="The question that this is an answer to")
    answer = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' on '.join([self.question.text, str(self.date)])
