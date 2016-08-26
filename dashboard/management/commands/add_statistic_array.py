from django.core.management.base import BaseCommand

from dashboard.models import Measurement


class Command(BaseCommand):
    help = 'Add statistical array to measurement.'

    def handle(self, *args, **options):
        import csv
        with open('R_scripts/bio_age/2016-08-26_2_means.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            header = next(reader)
            m = dict()
            for row in reader:
                mode = row[0].split('_')[-3]
                name = row[0].split('_')[-2]
                unit = row[0].split('_')[-1]
                new_name = name + '_' + unit
                m.setdefault(new_name, [list(map(float, header[1:])), [], []])
                if mode == 'sd':
                    m[new_name][2] = list(map(float, row[1:]))
                if mode == 'mean':
                    m[new_name][1] = list(map(float, row[1:]))

            for key, value in m.items():
                try:
                    name = key.split('_')[-2]
                    unit = key.split('_')[-1]
                    mes = Measurement.objects.get(slug_name=name, unit__abbreviation=unit)
                    mes.statistic_array = value
                    mes.save()
                except Measurement.DoesNotExist:
                    pass

