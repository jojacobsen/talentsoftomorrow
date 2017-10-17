import django_excel as excel
from datetime import date
from rest_framework import exceptions
import collections

from accounts.models import Player


def create_measurement_array(measurements, players):
    measurements_array = list()
    for m in measurements:
        for p in players:
            template_line = [
                p.id,
                p.first_name + ' ' + p.last_name,
                m.id,
                m.name,
                '',
                m.unit.name,
                date.today(),
                '',
            ]
            measurements_array.append(template_line)
    return measurements_array


def create_height_array(players, length_unit):
    height_array = list()
    for p in players:
        template_line = [
            p.id,
            p.first_name + ' ' + p.last_name,
            '',
            length_unit,
            date.today(),
        ]
        height_array.append(template_line)
    return height_array


def create_weight_array(players, weight_unit):
    height_array = list()
    for p in players:
        template_line = [
            p.id,
            p.first_name + ' ' + p.last_name,
            '',
            weight_unit,
            date.today(),
        ]
        height_array.append(template_line)
    return height_array


def create_excel_template(request):
    group = request.user.groups.values_list('name', flat=True)

    if 'Club' in group:
        measurements = request.user.club.measurements.filter()
        players = Player.objects.filter(club=request.user.club, archived=False)
        measurement_system = request.user.club.measurement_system

    elif 'Coach' in group:
        measurements = request.user.coach.club.measurements.filter()
        players = Player.objects.filter(club=request.user.coach.club, archived=False)
        measurement_system = request.user.coach.club
    else:
        raise exceptions.PermissionDenied('User has no permission to access user data of player.')

    if measurement_system == 'SI':
        weight_unit = 'kg'
        length_unit = 'cm'
    elif measurement_system == 'Imp':
        weight_unit = 'lb'
        length_unit = 'inch'

    performance = excel.pe.Sheet(create_measurement_array(measurements, players),
                                 name='Performance',
                                 colnames=[
                                  'player',
                                  'player name',
                                  'measurement',
                                  'measurement name',
                                  'value',
                                  'unit',
                                  'date',
                                  'description']
                                 )
    height = excel.pe.Sheet(create_height_array(players, length_unit),
                            name='Height',
                            colnames=[
                                 'player',
                                 'player name',
                                 'height',
                                 'unit',
                                 'date']
                            )
    weight = excel.pe.Sheet(create_height_array(players, weight_unit),
                            name='Weight',
                            colnames=[
                                'player',
                                'player name',
                                'weight',
                                'unit',
                                'date']
                            )

    sitting_height = excel.pe.Sheet(create_height_array(players, length_unit),
                            name='Sitting Height',
                            colnames=[
                                'player',
                                'player name',
                                'sitting_height',
                                'unit',
                                'date']
                            )
    sheets = {
        'Performance': performance,
        'Height': height,
        'Weight': weight,
        'Sitting Height': sitting_height,
    }
    book = excel.pe.Book(sheets=collections.OrderedDict(sheets))
    return book