from accounts.models import Player
from profile.models import SittingHeight, ParentsHeight, Weight, Height
from profile.serializers import PlayerProfileSerializer, HeightSerializer, \
    WeightSerializer, ParentsHeightSerializer, SittingHeightSerializer, BodyFatSerializer
from .filters import HeightFilter, WeightFilter, SittingHeightFilter, ParentsHeightFilter

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics, exceptions
from django.http import HttpResponse
from rest_framework import filters


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class PlayerProfileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PlayerProfileSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get(self, request, pk=None):
        group = self.request.user.groups.values_list('name', flat=True)
        if 'Club' in group:
            queryset = Player.objects.get(pk=pk, club=self.request.user.club, archived=False)
        elif 'Coach' in group:
            queryset = Player.objects.get(pk=pk, club=self.request.user.coach.club, archived=False)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')

        serializer = PlayerProfileSerializer(queryset)
        return JSONResponse(serializer.data)


class HeightCreateView(generics.CreateAPIView):
    """
    Creates Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = HeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class WeightCreateView(generics.CreateAPIView):
    """
    Creates Weight object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class ParentsHeightCreateView(generics.CreateAPIView):
    """
    Creates Parents Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ParentsHeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class SittingHeightCreateView(generics.CreateAPIView):
    """
    Creates Sitting Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SittingHeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class BodyFatCreateView(generics.CreateAPIView):
    """
    Creates Bodyfat object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = BodyFatSerializer
    # Parse JSON
    parser_classes = (JSONParser,)


class HeightView(generics.RetrieveUpdateDestroyAPIView):
    """
    Deletes Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = HeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Height.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Height.objects.filter(pk=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class WeightView(generics.RetrieveUpdateDestroyAPIView):
    """
    Deletes Weight object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Weight.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Weight.objects.filter(pk=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class ParentsHeightView(generics.RetrieveUpdateDestroyAPIView):
    """
    Deletes Parents Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ParentsHeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = ParentsHeight.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = ParentsHeight.objects.filter(pk=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class SittingHeightView(generics.RetrieveUpdateDestroyAPIView):
    """
    Deletes Sitting Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SittingHeightSerializer
    # Parse JSON
    parser_classes = (JSONParser,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = SittingHeight.objects.filter(pk=pk, player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = SittingHeight.objects.filter(pk=pk, player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class HeightListView(generics.ListAPIView):
    """
    List of Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = HeightSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    # Parse JSON
    parser_classes = (JSONParser,)
    filter_class = HeightFilter

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Height.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Height.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class WeightListView(generics.ListAPIView):
    """
    List of Weight object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WeightSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    # Parse JSON
    parser_classes = (JSONParser,)
    filter_class = WeightFilter

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = Weight.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = Weight.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class ParentsHeightListView(generics.ListAPIView):
    """
    List of Parents Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ParentsHeightSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    # Parse JSON
    parser_classes = (JSONParser,)
    filter_class = ParentsHeightFilter

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = ParentsHeight.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = ParentsHeight.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset


class SittingHeightListView(generics.ListAPIView):
    """
    List of Sitting Height object.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = SittingHeightSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter,)
    # Parse JSON
    parser_classes = (JSONParser,)
    filter_class = SittingHeightFilter

    def get_queryset(self):
        group = self.request.user.groups.values_list('name', flat=True)

        if 'Club' in group:
            queryset = SittingHeight.objects.filter(player__club=self.request.user.club)
        elif 'Coach' in group:
            queryset = SittingHeight.objects.filter(player__club=self.request.user.coach.club)
        else:
            raise exceptions.PermissionDenied('User has no permission to access user data of player.')
        return queryset
