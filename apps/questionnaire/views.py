from questionnaire.models import Questionnaire, Submission, Question
from .forms import SubmissionCreateForm
from .filters import SubmissionFilter
from .serializers import SubmissionSerializer, QuestionnaireSerializer

from django.shortcuts import redirect
from django.contrib import messages
from django.views import generic
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from rest_framework import filters
from django.utils.translation import ugettext as _


class QuestionnaireFormView(generic.DetailView):
    model = Questionnaire
    template_name = 'questionnaire/wizard.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireFormView, self).get_context_data(**kwargs)
        context['menu_item'] = kwargs['object'].slug
        return context


class QuestionnaireView(generic.ListView):
    model = Questionnaire
    template_name = 'questionnaire/overview.html'

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            return Questionnaire.objects.filter(club=self.request.user.club)
        elif 'Coach' in group:
            return Questionnaire.objects.filter(club=self.request.user.coach.club)
        elif 'Player' in group:
            return Questionnaire.objects.filter(club=self.request.user.player.club)
        else:
            raise PermissionDenied('User has no permission to access user data of player.')

    def get_context_data(self, **kwargs):
        context = super(QuestionnaireView, self).get_context_data(**kwargs)
        context['menu_item'] = 'questionnaire'
        return context


class SubmissionView(generic.ListView):
    model = Submission
    template_name = 'questionnaire/history.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Player' in group:
            return Submission.objects.filter(player=self.request.user.player, questionnaire__slug=slug)
        else:
            raise PermissionDenied('User has no permission to access user data of player.')

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super(SubmissionView, self).get_context_data(**kwargs)
        try:
            context['questionnaire'] = Questionnaire.objects.get(slug=slug)
        except Questionnaire.DoesNotExist as e:
            raise e
        context['menu_item'] = slug + '-history'
        return context


class SubmissionCreateView(generic.base.View):
    def post(self, request, slug):
        try:
            questions = Question.objects.filter(section__questionnaire__slug=slug)
        except Question.DoesNotExist as e:
            raise e
        form = SubmissionCreateForm(request.POST or None, extra=questions)
        if form.is_valid():
            form.save(player=self.request.user.player, questionnaire=questions[0].section.questionnaire)
            messages.add_message(request, messages.INFO, _('Your Questionnaire has been saved!'))
            return redirect('questionnaire:history', slug=slug)
        return redirect('questionnaire:wizard', slug=slug)


class SubmissionListView(generics.ListAPIView):
    """
    List all Submissions of players in club.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SubmissionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SubmissionFilter
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Submission.objects.filter(player__club=self.request.user.club).order_by('-created')
        elif 'Coach' in group:
            queryset = Submission.objects.filter(player__club=self.request.user.coach.club).order_by('-created')
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class QuestionnaireListView(generics.ListAPIView):
    """
    List all Questionnaires in a club.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = QuestionnaireSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Questionnaire.objects.filter(club=self.request.user.club).order_by('name')
        elif 'Coach' in group:
            queryset = Questionnaire.objects.filter(club=self.request.user.coach.club).order_by('name')
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset
