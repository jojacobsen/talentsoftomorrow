from unittest import mock
import unittest
import decimal
from django.conf import settings
import datetime


class TestInterpolate(unittest.TestCase):
    def test_interpolate(self):
        from apps.analysis.calculate import Interpolate
        age = 14.386
        statistic_array = [[9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5],
                           [4.528541667, 4.505416667, 4.482291667, 4.459166667, 4.436041667, 4.412916667, 4.389791667,
                            4.366666667, 4.343541667, 4.320416667, 4.297291667, 4.274166667, 4.246041667, 4.217916667,
                            4.189791667, 4.161666667, 4.133541667],
                           [0.263276455, 0.263068882, 0.262861309, 0.262653736, 0.262446162, 0.262238589, 0.262031016,
                            0.261823443, 0.261615869, 0.261408296, 0.261200723, 0.26099315, 0.224285769, 0.187578388,
                            0.150871006, 0.114163625, 0.077456244]]
        i = Interpolate(statistic_array[0], statistic_array[1])
        population_mean = i[age]
        self.assertEquals(4.302564167, population_mean)
        i = Interpolate(statistic_array[0], statistic_array[2])
        population_sd = i[age]
        self.assertEquals(0.261248049644, population_sd)


class TestPythonAnalysis(unittest.TestCase):
    def test_get_alternative_bio_age(self):
        from apps.analysis.calculate import PythonAnalysis
        current_age = 14
        phv_age = 14
        p = PythonAnalysis()
        bio_age = p.get_alternative_bio_age(current_age, phv_age)
        self.assertEquals(decimal.Decimal(14), bio_age)


class TestRscripts(unittest.TestCase):
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
            self.assertEquals(decimal.Decimal(17.5), age)

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


class TestSignals(unittest.TestCase):
    @mock.patch('apps.analysis.signals.handlers.PredictedHeight')
    def test_post_khamis_roche_handler(self, mock_predictedheight):
        from apps.analysis.signals.handlers import post_khamis_roche_handler
        sender = mock.MagicMock()
        instance = mock.MagicMock()
        mock_predictedheight.objects.create.return_value = mock.MagicMock()
        post_khamis_roche_handler(sender, instance, created=True)
        mock_predictedheight.objects.create.assert_called_with(player=instance.player,
                                                               date=instance.date,
                                                               predicted_height=instance.predicted_height,
                                                               method='khr',
                                                               khamis_roche=instance,
                                                               dna_height=None)
        post_khamis_roche_handler(sender, instance, created=False)
        instance.player.predictedheight_set.filter.assert_called_with(khamis_roche=instance)


class TestBenchmark(unittest.TestCase):
    @mock.patch('apps.analysis.benchmark.utils.abs')
    @mock.patch('apps.analysis.benchmark.utils.Benchmark')
    @mock.patch('apps.analysis.benchmark.utils.RscriptAnalysis')
    def test_create_benchmark(self, mock_rscriptanalysis, mock_benchmark, mock_abs):
        from apps.analysis.benchmark.utils import Performance
        from apps.analysis.benchmark.utils import create_benchmark
        sender = mock.MagicMock()
        instance = mock.MagicMock()
        instance.date = datetime.date.today()
        success = create_benchmark(sender, instance, True)
        # Should only work if sender is Performance
        self.assertEquals(success, False)
        sender = Performance
        mock_abs.return_value = 5
        instance.player.bioage_set.filter.latest.return_value = mock.MagicMock()
        mock_rscriptanalysis.get_benchmark.return_value = mock.MagicMock()
        mock_benchmark.objects.create.return_value = mock.MagicMock()
        success = create_benchmark(sender, instance, True)
        self.assertEquals(success, True)
        success = create_benchmark(sender, instance, False)
        self.assertEquals(success, True)


class TestBioAge(unittest.TestCase):
    @mock.patch('apps.analysis.bio_age.utils.BioAge')
    @mock.patch('apps.analysis.bio_age.utils.RscriptAnalysis')
    def test_create_bio_age(self, mock_rscriptanalysis, mock_bioage):
        from apps.analysis.bio_age.utils import create_bio_age
        from apps.analysis.bio_age.utils import PredictedHeight
        sender = mock.MagicMock()
        instance = mock.MagicMock()
        success = create_bio_age(sender, instance, True)
        self.assertEquals(success, False)
        mock_rscriptanalysis.return_value.get_bio_age.return_value = [decimal.Decimal(15), []]
        mock_bioage.objects.create.return_value = mock.MagicMock()
        instance.player.predictedheight_set.filter.return_value.latest.return_value = instance
        success = create_bio_age(sender, instance, True)
        self.assertEquals(success, True)
        success = create_bio_age(sender, instance, False)
        self.assertEquals(success, True)
        instance.player.predictedheight_set.filter.return_value.latest.side_effect = PredictedHeight.DoesNotExist
        success = create_bio_age(sender, instance, False)
        self.assertEquals(success, False)

    @mock.patch('apps.analysis.bio_age.utils.BioAge')
    @mock.patch('apps.analysis.bio_age.utils.PythonAnalysis')
    def test_create_alternative_bio_age(self, mock_pythonanalysis, mock_bioage):
        from apps.analysis.bio_age.utils import create_alternative_bio_age
        from apps.analysis.bio_age.utils import PHV
        sender = mock.MagicMock()
        instance = mock.MagicMock()
        success = create_alternative_bio_age(sender, instance, True)
        self.assertEquals(success, False)
        sender = PHV
        instance.player.bioage_set.filter.return_value.values_list.return_value = None
        mock_pythonanalysis.return_value.get_alternative_bio_age.return_value = decimal.Decimal(15)
        mock_bioage.objects.create.return_value = mock.MagicMock()
        success = create_alternative_bio_age(sender, instance, True)
        self.assertEquals(success, True)
        success = create_alternative_bio_age(sender, instance, False)
        self.assertEquals(success, True)


class TestKhamisRoche(unittest.TestCase):
    @mock.patch('apps.analysis.khamis_roche.utils.round')
    @mock.patch('apps.analysis.khamis_roche.utils.KhamisRoche')
    @mock.patch('apps.analysis.khamis_roche.utils.RscriptAnalysis')
    def test_create_bio_age(self, mock_rscriptanalysis, mock_khr, mock_round):
        from apps.analysis.khamis_roche.utils import create_khamis_roche
        from apps.analysis.khamis_roche.utils import Height
        sender = Height
        instance = mock.MagicMock()
        mock_round.return_value = 14.5
        mock_khr.objects.create.return_value = mock.MagicMock()
        mock_rscriptanalysis.return_value.get_khamis_roche.return_value = [decimal.Decimal(186), {}]
        success = create_khamis_roche(sender, instance, True)
        self.assertEquals(success, True)
        success = create_khamis_roche(sender, instance, False)
        self.assertEquals(success, True)
        mock_rscriptanalysis.return_value.get_khamis_roche.return_value = [None, None]
        success = create_khamis_roche(sender, instance, False)
        self.assertEquals(success, False)


class TestMirwald(unittest.TestCase):
    @mock.patch('apps.analysis.mirwald.utils.PHV')
    @mock.patch('apps.analysis.mirwald.utils.RscriptAnalysis')
    def test_create_phv(self, mock_rscriptanalysis, mock_phv):
        from apps.analysis.mirwald.utils import create_phv
        from apps.analysis.mirwald.utils import Height
        sender = Height
        instance = mock.MagicMock()
        mock_phv.objects.create.return_value = mock.MagicMock()
        mock_rscriptanalysis.return_value.get_phv.return_value = 1.8
        success = create_phv(sender, instance, True)
        self.assertEquals(success, True)
        success = create_phv(sender, instance, False)
        self.assertEquals(success, True)
