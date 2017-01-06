from unittest import mock
import unittest
import decimal
from django.conf import settings


class TestCalculate(unittest.TestCase):
    if settings.R_AVAILABLE:
        def test_get_bio_age(self):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            predicted_height = 180
            current_height = 140
            age, slope = r.get_bio_age(predicted_height, current_height, country='uk')
            self.assertEquals(decimal.Decimal(9.75), age)
            predicted_height = 140
            current_height = 180
            age, slope = r.get_bio_age(predicted_height, current_height, country='uk')
            self.assertEquals(decimal.Decimal(18), age)

        @mock.patch('apps.analysis.calculate.Interpolate')
        def test_get_benchmark(self, mock_interpolate):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            value = 9
            age = 3
            statistic_array = mock.MagicMock()
            mock_interpolate.return_value = [5, 6, 7, 8, 9, 10]
            benchmark = r.get_benchmark(value, age, statistic_array, False)
            self.assertEquals(decimal.Decimal(55), benchmark)

        def test_get_khamis_roche(self):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            current_height = 140
            current_age = 10
            current_weight = 50
            fathers_height = 185
            mothers_height = 176
            gender = 'Male'
            predicted_height, meta = r.get_khamis_roche(current_height, current_age, current_weight, fathers_height,
                                           mothers_height, gender)
            self.assertEquals(190.6294, predicted_height.cm)

        def test_get_phv(self):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            current_height = 157.0
            current_age = 12.084
            current_weight = 53.0
            sitting_height = 79.6
            phv_delta = r.get_phv(current_height, current_age, current_weight, sitting_height)
            self.assertEquals(-1.408292, phv_delta)

    else:
        # Needed to find a solution for CircleCi (doesn't support R!!)
        @mock.patch('apps.analysis.calculate.subprocess')
        def test_get_bio_age(self, mock_subprocess):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            mock_subprocess.Popen.communicate.return_value = mock.MagicMock()
            predicted_height = 180
            current_height = 140
            r.get_bio_age(predicted_height, current_height, country='uk')

        @mock.patch('apps.analysis.calculate.subprocess')
        @mock.patch('apps.analysis.calculate.Interpolate')
        def test_get_benchmark(self, mock_interpolate, mock_subprocess):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            value = 9
            age = 3
            statistic_array = mock.MagicMock()
            mock_interpolate.return_value = [5, 6, 7, 8, 9, 10]
            mock_subprocess.Popen.communicate.return_value = mock.MagicMock()
            r.get_benchmark(value, age, statistic_array, False)

        @mock.patch('apps.analysis.calculate.subprocess')
        def test_get_khamis_roche(self, mock_subprocess):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            current_height = 140
            current_age = 10
            current_weight = 50
            fathers_height = 185
            mothers_height = 176
            gender = 'Male'
            mock_subprocess.Popen.communicate.return_value = mock.MagicMock()
            r.get_khamis_roche(current_height, current_age, current_weight, fathers_height,
                                           mothers_height, gender)

        @mock.patch('apps.analysis.calculate.subprocess')
        def test_get_phv(self, mock_subprocess):
            from apps.analysis.calculate import RscriptAnalysis
            r = RscriptAnalysis()
            current_height = 157.0
            current_age = 12.084
            current_weight = 53.0
            sitting_height = 79.6
            mock_subprocess.Popen.communicate.return_value = mock.MagicMock()
            r.get_phv(current_height, current_age, current_weight, sitting_height)

