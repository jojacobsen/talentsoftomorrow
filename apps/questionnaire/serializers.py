import datetime
from rest_framework import serializers
from questionnaire.models import Questionnaire


class SubmissionSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        answers = list()
        for a in instance.answer_set.filter():
            answers.append({
                'question': a.question.text,
                'question_type': a.question.question_type,
                'question_id': a.question.id,
                'question_slug': a.question.slug,
                'question_sort': a.question.sort,
                'answer': a.answer,
                'section': {
                    'heading': a.question.section.heading,
                    'id': a.question.section.id,
                    'sort': a.question.section.sort
                }
            })
        if answers:
            answers = sorted(answers, key=lambda k: k['question_sort'])
        return {
            'id': instance.id,
            'created': instance.created,
            'date': instance.date,
            'questionnaire': instance.questionnaire.name,
            'questionnaire_id': instance.questionnaire.id,
            'player': instance.player.id,
            'answers': answers
        }


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
