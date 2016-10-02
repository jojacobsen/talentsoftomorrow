import subprocess
import decimal
import logging
from django.conf import settings
from bisect import bisect_left

logger = logging.getLogger(__name__)


class Interpolate(object):
    def __init__(self, x_list, y_list):
        if any(y - x <= 0 for x, y in zip(x_list, x_list[1:])):
            raise ValueError("x_list must be in strictly ascending order!")
        x_list = self.x_list = list(map(float, x_list))
        y_list = self.y_list = list(map(float, y_list))
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1)/(x2 - x1) for x1, x2, y1, y2 in intervals]

    def __getitem__(self, x):
        i = bisect_left(self.x_list, x) - 1
        return self.y_list[i] + self.slopes[i] * (x - self.x_list[i])


class RscriptAnalysis(object):
    def __init__(self):
        self.r_folder = settings.BASE_DIR + "/R_scripts"

        self.height_prediction_command = self.r_folder + "/bio_age/2016-07-14_bioage_calculator.R"
        self.benchmark_command = self.r_folder + "/bio_age/2016-08-04_benchmark_calculator.R"

    def get_bio_age(self, predicted_height, current_height, country='uk'):
        if country == 'uk':
            average_height_data = self.r_folder + '/bio_age/2016-07-06_Heigh_prediction_data_google_doc_extract.xlsx'

        if current_height < predicted_height:
            bash_command = " ".join([self.height_prediction_command, str(predicted_height), str(current_height),
                                    average_height_data])
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output = str(process.communicate()[0])
            results = output.split('\\n')
            try:
                bio_age = decimal.Decimal(results[1])
            except IndexError:
                logger.warning('Could not calculate bio age for %s (predicted height) and %s (current height)!'
                               % (str(predicted_height), str(current_height)))
                bio_age = None
                slope = None
                return bio_age, slope

            slope = list()

            x_slope = [float(i) for i in results[3].split()]
            y_slope = [float(i) for i in results[5].split()]

            for i in range(0, len(x_slope)):
                slope.append([x_slope[i], y_slope[i]])

        else:
            bio_age = 18
            slope = [[18, float(current_height)]]

        return bio_age, slope

    def get_benchmark(self, value, age, statistic_array, smaller_is_better):
        i = Interpolate(statistic_array[0], statistic_array[1])
        population_mean = i[age]
        i = Interpolate(statistic_array[0], statistic_array[2])
        population_sd = i[age]

        if smaller_is_better:
            direction = 'downBetter'
        else:
            direction = 'upBetter'
        bash_command = " ".join([self.benchmark_command, str(value), str(population_mean),
                                str(population_sd), direction])
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output = str(process.communicate()[0])
        results = output.split('\\n')
        return decimal.Decimal(results[1][:-1])
