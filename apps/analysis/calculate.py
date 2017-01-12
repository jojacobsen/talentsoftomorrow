import subprocess
import decimal
import logging
from django.conf import settings
from bisect import bisect_left
from measurement.measures import Distance

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
        # Where to look for R scripts
        self.r_folder = settings.PROJECT_ROOT + "/apps/analysis"

        # Bio age scripts
        self.height_prediction_command = self.r_folder + "/bio_age/bioage_calculator.R"

        # Benchmark scripts
        self.benchmark_command = self.r_folder + "/benchmark/benchmark_calculator.R"

        # KHR scripts
        self.khamis_roche_command = self.r_folder + "/khamis_roche/khamis_roche.R"
        self.coefficients_file_khr = self.r_folder + "/khamis_roche/khamis_roche_coefficents.txt"

        # PHV scripts
        self.phv_command = self.r_folder + "/mirwald/Mirwald.R"

    def get_bio_age(self, predicted_height, current_height, country='uk'):
        """
        Calculates biological age based on predicted height and current height. Is country specific (currently only UK
        supported).
        :param predicted_height:
        :param current_height:
        :param country:
        :return bio_age:
        :return slope:
        """
        if country == 'uk':
            pass
        else:
            logger.error('Other countries than UK not implemented yet!')
            bio_age = None
            slope = None
            return bio_age, slope

        if current_height < predicted_height:
            # Swoop....prediction should be higher than current height
            bash_command = " ".join([self.height_prediction_command, str(predicted_height), str(current_height)])
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output = str(process.communicate()[0])
            results = output.split('\\n')
            try:
                bio_age = decimal.Decimal(results[1])
            except IndexError:
                logger.error('Could not calculate bio age for %s (predicted height) and %s (current height)!'
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
            # Otherwise just take current height as predicted height, because we are always right!
            bio_age = decimal.Decimal(18)
            slope = [[18, float(current_height)]]

        return bio_age, slope

    def get_benchmark(self, value, age, statistic_array, smaller_is_better):
        """
        Calculates benchmark based on age.
        :param value:
        :param age:
        :param statistic_array:
        :param smaller_is_better:
        :return benchmark:
        """
        # statistic_array[0]: Age
        # statistic_array[1]: Average
        # statistic_array[2]: SD
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
        try:
            benchmark = decimal.Decimal(results[1][:-1])
        except IndexError:
            logger.error('Could not benchmark for values:'
                         ' %s (value),'
                         ' %s (age),'
                         ' %s (statistic_array),'
                         ' %s (smaller_is_better).'
                         % (str(value), str(age), str(statistic_array), str(smaller_is_better)))
            benchmark = None
        return benchmark

    def get_khamis_roche(self, current_height, current_age, current_weight, fathers_height, mothers_height, gender):
        """
        Calculates adults height based on Khamis Roche method.
        :param current_height:
        :param current_age:
        :param current_weight:
        :param fathers_height:
        :param mothers_height:
        :param gender:
        :return predicted_height:
        :return mean_absolute_deviation_50:
        :return mean_absolute_deviation_90:
        """
        bash_command = " ".join([self.khamis_roche_command, str(current_height), str(current_age), str(current_weight),
                                 str(mothers_height), str(fathers_height), gender, self.coefficients_file_khr])
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output = str(process.communicate()[0])
        results = output.split('\\n')
        try:
            predicted_height = Distance(cm=float(results[1]))
            meta = {
                'mean_absolute_deviation_50': results[3],
                'mean_absolute_deviation_90': results[5]
            }
        except IndexError:
            logger.error('Could not calculate khr with following values: '
                         '%s (current_height), '
                         '%s (current_age),'
                         '%s (current_weight),'
                         '%s (mothers_height),'
                         '%s (fathers_height).'
                         % (str(current_height), str(current_age), str(current_weight),
                            str(mothers_height), str(fathers_height)))
            predicted_height = None
            meta = {}

        return predicted_height, meta

    def get_phv(self, current_height, current_age, current_weight, sitting_height):
        """
        Calculates peak of growth spurt (PHV) based on the Mirwald method.
        :param current_height:
        :param current_age:
        :param current_weight:
        :param sitting_height:
        :return phv_delta: Distance to PHV in Years
        """
        bash_command = " ".join([self.phv_command, str(current_age), str(current_height), str(current_weight),
                                 str(sitting_height)])
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output = str(process.communicate()[0])
        results = output.split('\\n')
        try:
            phv_delta = float(results[1])
        except IndexError:
            logger.error('Could not calculate khr with following values: '
                         '%s (current_height), '
                         '%s (current_age),'
                         '%s (current_weight),'
                         '%s (sitting_height),'
                         % (str(current_height), str(current_age), str(current_weight),
                            str(sitting_height)))
            phv_delta = None
        return phv_delta  # Distance to PHV in Years
