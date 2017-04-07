from django.contrib import admin
from questionnaire.models import Questionnaire, Question, Section, Answer, Submission

admin.site.register(Questionnaire)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Submission)
