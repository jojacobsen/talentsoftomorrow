from django.contrib import admin
from questionnaire.models import Questionnaire, Question, Choice, Section, Answer, Submission


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['club']
    search_fields = ['name', 'slug']


class SectioneAdmin(admin.ModelAdmin):
    list_display = ['questionnaire', 'heading', 'sort']
    list_filter = ['questionnaire']
    search_fields = ['heading', 'questionnaire__name']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_questionnaire', 'question_type', 'slug', 'sort', 'required']
    list_filter = ['section__questionnaire', 'section', 'required']
    search_fields = ['heading', 'questionnaire__name', 'slug']

    def get_questionnaire(self, obj):
        return obj.section.questionnaire.name
    get_questionnaire.short_description = 'Questionnaire'  # Renames column head


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'get_question', 'get_questionnaire', 'get_question_type', 'value', 'sort']
    list_filter = ['question__section__questionnaire']
    search_fields = ['text', 'value']

    def get_question(self, obj):
        return obj.question.text
    get_question.short_description = 'Question'  # Renames column head

    def get_question_type(self, obj):
        return obj.question.question_type
    get_question_type.short_description = 'Question Type'  # Renames column head

    def get_questionnaire(self, obj):
        return obj.question.section.questionnaire.name
    get_questionnaire.short_description = 'Questionnaire'  # Renames column head


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['player', 'questionnaire', 'date', 'created']
    list_filter = ['questionnaire', 'player__club__name', 'date', 'created']
    search_fields = ['questionnaire__name', 'player__first_name', 'player__last_name', 'player__user__username']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['get_player', 'question', 'answer', 'date', 'created']
    list_filter = ['submission__questionnaire', 'submission__player__club__name', 'date', 'created', 'question']
    search_fields = ['submission__questionnaire__name', 'submission__player__first_name',
                     'submission__player__last_name', 'player__user__username', 'answer', 'question__text']

    def get_player(self, obj):
        return obj.submission.player
    get_player.short_description = 'Player'  # Renames column head

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Section, SectioneAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Answer, AnswerAdmin)

