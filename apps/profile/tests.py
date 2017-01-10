from unittest import mock
import unittest


class TestViews(unittest.TestCase):
    @mock.patch('apps.profile.views.JSONRenderer')
    def test_jsonresponse(self, mock_jsonrenderer):
        from apps.profile.views import JSONResponse
        content = mock.MagicMock()
        mock_jsonrenderer.return_value.render.return_value = content
        data = mock.MagicMock()
        response = JSONResponse(data)
        self.assertEquals(response.status_code, 200)


class TestSerializers(unittest.TestCase):
    @mock.patch('apps.profile.serializers.round')
    def test_playerprofileserializer(self, mock_round):
        from apps.profile.serializers import PlayerProfileSerializer
        obj = mock.MagicMock()
        view = mock.MagicMock()
        height = mock.MagicMock()
        weight = mock.MagicMock()
        s_height = mock.MagicMock()
        prediction = mock.MagicMock()
        parents_height = mock.MagicMock()
        current_height = 155.0
        predicted_height = 185.0
        fathers_height = 182.0
        mothers_height = 178.0
        height_unit = 'cm'
        sitting_height = 155.0
        current_weight = 45.0
        weight_unit = 'kg'
        height.value_club_unit.return_value = [current_height, height_unit]
        obj.height_set.filter.return_value.latest.return_value = height
        weight.value_club_unit.return_value = [current_weight, weight_unit]
        obj.weight_set.filter.return_value.latest.return_value = weight
        s_height.value_club_unit.return_value = [sitting_height, height_unit]
        obj.sittingheight_set.filter.return_value.latest.return_value = s_height
        prediction.value_club_unit.return_value = [predicted_height, height_unit]
        obj.predictedheight_set.filter.return_value.latest.return_value = prediction
        parents_height.value_club_unit.return_value = [fathers_height, mothers_height, height_unit]
        obj.parentsheight_set.filter.return_value.latest.return_value = parents_height
        age = 14.5
        mock_round.return_value = age
        serializer = PlayerProfileSerializer(context={'view': view})
        validated_data = serializer.to_representation(obj)
        self.assertEquals(validated_data['player'], obj.id)
        self.assertEquals(validated_data['mothers_height'], mothers_height)
        self.assertEquals(validated_data['fathers_height'], fathers_height)
        self.assertEquals(validated_data['height_unit'], height_unit)
        self.assertEquals(validated_data['weight_unit'], weight_unit)
        self.assertEquals(validated_data['sitting_height'], sitting_height)
        self.assertEquals(validated_data['current_weight'], current_weight)
        self.assertEquals(validated_data['predicted_height'], predicted_height)
        self.assertEquals(validated_data['current_height'], current_height)

    def test_heightserializervalidate(self):
        from apps.profile.serializers import HeightSerializer
        request = mock.MagicMock()
        club = mock.MagicMock()
        data = dict()
        data['height'] = 150.0
        data['unit'] = 'cm'
        request.user.club = club
        data['player'] = mock.MagicMock(club=club)
        request.user.groups.values_list.return_value = 'Club'
        serializer = HeightSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['player'].club, club)
        self.assertEquals(validated_data['height'], data['height'])
        data['height'] = 60.0
        data['unit'] = 'inch'
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['height'], data['height'])

    def test_heightserializerrepresent(self):
        from apps.profile.serializers import HeightSerializer
        instance = mock.MagicMock()
        serializer = HeightSerializer()
        current_height = 155.0
        height_unit = 'cm'
        instance.value_club_unit.return_value = [current_height, height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['height'], current_height)
        self.assertEquals(represent_data['unit'], height_unit)
        self.assertEquals(represent_data['player'], instance.player.id)
        self.assertEquals(represent_data['date'], instance.date)
        current_height = 60.0
        height_unit = 'inch'
        instance.value_club_unit.return_value = [current_height, height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['height'], current_height)
        self.assertEquals(represent_data['unit'], height_unit)

    def test_weightserializervalidate(self):
        from apps.profile.serializers import WeightSerializer
        request = mock.MagicMock()
        club = mock.MagicMock()
        data = dict()
        data['weight'] = 50.0
        data['unit'] = 'kg'
        request.user.club = club
        data['player'] = mock.MagicMock(club=club)
        request.user.groups.values_list.return_value = 'Club'
        serializer = WeightSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['player'].club, club)
        self.assertEquals(validated_data['weight'], data['weight'])
        data['weight'] = 100.0
        data['unit'] = 'lb'
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['weight'], data['weight'])

    def test_weightserializerrepresent(self):
        from apps.profile.serializers import WeightSerializer
        instance = mock.MagicMock()
        serializer = WeightSerializer()
        current_weight = 50.0
        weight_unit = 'kg'
        instance.value_club_unit.return_value = [current_weight, weight_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['weight'], current_weight)
        self.assertEquals(represent_data['unit'], weight_unit)
        self.assertEquals(represent_data['player'], instance.player.id)
        self.assertEquals(represent_data['date'], instance.date)
        current_weight = 100.0
        weight_unit = 'lb'
        instance.value_club_unit.return_value = [current_weight, weight_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['weight'], current_weight)
        self.assertEquals(represent_data['unit'], weight_unit)

    def test_sittingheightserializervalidate(self):
        from apps.profile.serializers import SittingHeightSerializer
        request = mock.MagicMock()
        club = mock.MagicMock()
        data = dict()
        data['sitting_height'] = 80.3
        data['unit'] = 'cm'
        request.user.club = club
        data['player'] = mock.MagicMock(club=club)
        request.user.groups.values_list.return_value = 'Club'
        serializer = SittingHeightSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['player'].club, club)
        self.assertEquals(validated_data['sitting_height'], data['sitting_height'])
        data['sitting_height'] = 30.4
        data['unit'] = 'inch'
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['sitting_height'], data['sitting_height'])

    def test_sittingheightserializerrepresent(self):
        from apps.profile.serializers import SittingHeightSerializer
        instance = mock.MagicMock()
        serializer = SittingHeightSerializer()
        sitting_height = 80.0
        height_unit = 'cm'
        instance.value_club_unit.return_value = [sitting_height, height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['sitting_height'], sitting_height)
        self.assertEquals(represent_data['unit'], height_unit)
        self.assertEquals(represent_data['player'], instance.player.id)
        self.assertEquals(represent_data['date'], instance.date)
        sitting_height = 30.0
        height_unit = 'inch'
        instance.value_club_unit.return_value = [sitting_height, height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['sitting_height'], sitting_height)
        self.assertEquals(represent_data['unit'], height_unit)

    def test_parentsheightserializervalidate(self):
        from apps.profile.serializers import ParentsHeightSerializer
        request = mock.MagicMock()
        club = mock.MagicMock()
        data = dict()
        data['fathers_height'] = 185.0
        data['mothers_height'] = 170.0
        data['unit'] = 'cm'
        request.user.club = club
        data['player'] = mock.MagicMock(club=club)
        request.user.groups.values_list.return_value = 'Club'
        serializer = ParentsHeightSerializer(context={'request': request})
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['player'].club, club)
        self.assertEquals(validated_data['fathers_height'], data['fathers_height'])
        self.assertEquals(validated_data['mothers_height'], data['mothers_height'])
        data['fathers_height'] = 73.0
        data['mothers_height'] = 67.0
        data['unit'] = 'inch'
        validated_data = serializer.validate(data)
        self.assertEquals(validated_data['fathers_height'], data['fathers_height'])
        self.assertEquals(validated_data['mothers_height'], data['mothers_height'])

    def test_parentsheightserializerrepresent(self):
        from apps.profile.serializers import ParentsHeightSerializer
        instance = mock.MagicMock()
        serializer = ParentsHeightSerializer()
        fathers_height = 185.0
        mothers_height = 170.0
        height_unit = 'cm'
        instance.value_club_unit.return_value = [fathers_height, mothers_height, height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['fathers_height'], fathers_height)
        self.assertEquals(represent_data['mothers_height'], mothers_height)
        self.assertEquals(represent_data['unit'], height_unit)
        self.assertEquals(represent_data['player'], instance.player.id)
        fathers_height = 73.0
        mothers_height = 67.0
        height_unit = 'inch'
        instance.value_club_unit.return_value = [fathers_height, mothers_height,height_unit]
        represent_data = serializer.to_representation(instance)
        self.assertEquals(represent_data['fathers_height'], fathers_height)
        self.assertEquals(represent_data['mothers_height'], mothers_height)
        self.assertEquals(represent_data['unit'], height_unit)
