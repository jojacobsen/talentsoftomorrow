import subprocess
import decimal
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class RscriptAnalysis(object):
    def __init__ (self):
        self.r_folder = settings.BASE_DIR + "/R_scripts"

        self.height_prediction_command = self.r_folder + "/bio_age/2016-07-14_bioage_calculator.R"

    def get_bio_age(self, predicted_height, current_height, country='uk'):
        if country == 'uk':
            average_height_data = self.r_folder + '/bio_age/2016-07-06_Heigh_prediction_data_google_doc_extract.xlsx'

        if current_height < predicted_height:
            bashCommand = " ".join([self.height_prediction_command, str(predicted_height), str(current_height), average_height_data])
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
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