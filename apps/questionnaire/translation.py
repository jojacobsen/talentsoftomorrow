from modeltranslation.translator import translator, TranslationOptions
from questionnaire.models import Questionnaire, Section, Question, Choice


class QuestionnaireTranslationOptions(TranslationOptions):
    fields = ('name', 'short_description',)


class SectionTranslationOptions(TranslationOptions):
    fields = ('heading',)


class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'input_placeholder', 'footer',)


class ChoiceTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(Questionnaire, QuestionnaireTranslationOptions)
translator.register(Section, SectionTranslationOptions)
translator.register(Question, QuestionTranslationOptions)
translator.register(Choice, ChoiceTranslationOptions)
