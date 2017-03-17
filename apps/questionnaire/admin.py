from django.contrib import admin
from questionnaire.models import Questionnaire, Question, Section, Answer

admin.site.register(Questionnaire)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Answer)
