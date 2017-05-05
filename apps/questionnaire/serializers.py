import datetime
from rest_framework import serializers
from questionnaire.models import Questionnaire


class SubmissionSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        answers = list()
        for a in instance.answer_set.filter():
            question = a.question
            answers.append({
                'question': question.text,
                'question_type': question.question_type,
                'question_id': question.id,
                'question_slug': question.slug,
                'question_sort': question.sort,
                'answer': a.answer,
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
