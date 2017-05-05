import datetime
from rest_framework import serializers
from questionnaire.models import Questionnaire


class SubmissionSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        answers = list()
        for a in instance.answer_set.values_list('answer', 'question__text', 'question__question_type',
                                                 'question__id', 'question__slug', 'question__sort').filter():
            answers.append({
                'question': a[1],
                'question_type': a[2],
                'question_id': a[3],
                'question_slug': a[4],
                'question_sort': a[5],
                'answer': a[0],
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
