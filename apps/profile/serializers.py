import datetime
from rest_framework import serializers, exceptions
from profile.models import Height, Weight, PredictedHeight, BioAge, ParentsHeight, SittingHeight, PHV
from measurement.measures import Distance
from measurement.measures import Weight as WeightMeasurement


class PlayerProfileSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        try:
            height = obj.height_set.filter().latest('date')
            height_date = height.date
            # Uses the date when height was recorded
            current_age = round((height_date - obj.birthday).days / 365.25, 1)
            current_height, height_unit = height.value_club_unit()
        except Height.DoesNotExist:
            height_unit = None
            current_height = None
            current_age = round((datetime.date.today() - obj.birthday).days / 365.25, 1)

        # Get latest weight record
        try:
            weight = obj.weight_set.filter().latest('date')
            current_weight, weight_unit = weight.value_club_unit()
        except Weight.DoesNotExist:
            current_weight = None
            weight_unit = None

        try:
            s_height = obj.sittingheight_set.filter().latest('date')
            sitting_height, height_unit = s_height.value_club_unit()
        except SittingHeight.DoesNotExist:
            sitting_height = None

        try:
            # DNA result always highest prio
            prediction, prediction_method = obj.predictedheight_set.filter(
                method='dna'
            ).latest('date')
            prediction_method = 'dna'
            predicted_height, height_unit = prediction.value_club_unit()
        except PredictedHeight.DoesNotExist:
            try:
                # If not DNA test, latest KHR result
                prediction = obj.predictedheight_set.filter(
                    method='khr'
                ).latest('date')
                prediction_method = 'khr'
                predicted_height, height_unit = prediction.value_club_unit()
            except PredictedHeight.DoesNotExist:
                # Return nada if not even KHR result
                predicted_height = None
                prediction_method = None

        # Get parents height
        try:
            parents_height = obj.parentsheight_set.filter().latest('created')
            fathers_height, mothers_height, height_unit = parents_height.value_club_unit()
        except ParentsHeight.DoesNotExist:
            fathers_height = None
            mothers_height = None

        try:
            # Latest BioAge is always the best
            bio_age = obj.bioage_set.values_list('bio_age', flat=True).latest('created')
        except BioAge.DoesNotExist:
            bio_age = None

        try:
            # Latest PHV is always the best
            phv_date = obj.phv_set.values_list('phv_date', flat=True).latest('date')
            phv_days = (phv_date - datetime.date.today()).days
            growth_spurt_start = phv_date - datetime.timedelta(days=90)  # 3 Month before PHV
            growth_position = 10 - phv_days / 365.25  # To display it in graph (10 is fixed value)
        except PHV.DoesNotExist:
            phv_date = None
            phv_days = None
            growth_spurt_start = None
            growth_position = None

        return {
            'player_id': obj.id,
            'player_name': obj.first_name + ' ' + obj.last_name,
            'lab_key': obj.lab_key,
            'gender': obj.gender,
            'birthday': obj.birthday,
            'current_height': current_height,
            'predicted_height': predicted_height,
            'prediction_method': prediction_method,
            'height_unit': height_unit,
            'height_date': height_date,
            'sitting_height': sitting_height,
            'current_weight': current_weight,
            'weight_unit': weight_unit,
            'bio_age': bio_age,
            'real_age': current_age,
            'fathers_height': fathers_height,
            'mothers_height': mothers_height,
            'phv_date': phv_date,
            'phv_days': phv_days,
            'growth_spurt_start': growth_spurt_start,
            'growth_position': growth_position,
        }


class HeightSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(allow_blank=False, max_length=10, required=True)

    class Meta:
        model = Height
        fields = ('player', 'date', 'height', 'unit')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if data['unit'] == 'cm':
            if 50 <= data['height'] <= 250:
                height = Distance(cm=data['height'])
            else:
                raise serializers.ValidationError('Height %s cm seems to be wrong.' % data['height'])
        elif data['unit'] == 'inch':
            if 20 <= data['height'] <= 100:
                height = Distance(inch=data['height'])
            else:
                raise serializers.ValidationError('Height %s inch seems to be wrong.' % data['height'])
        else:
            raise serializers.ValidationError('Field unit needs to be cm or inch!')
        data.pop('unit')
        data['height'] = height
        return data

    def to_representation(self, instance):
        height = instance.value_club_unit()[0]
        unit = instance.value_club_unit()[1]
        return {
            'height': height,
            'unit': unit,
            'date': instance.date,
            'player': instance.player.id
        }


class WeightSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(allow_blank=False, max_length=10, required=True)

    class Meta:
        model = Weight
        fields = ('player', 'date', 'weight', 'unit')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if data['unit'] == 'kg':
            if 20 <= data['weight'] <= 150:
                weight = WeightMeasurement(kg=data['weight'])
            else:
                raise serializers.ValidationError('Weight %s kg seems to be wrong.' % data['weight'])
        elif data['unit'] == 'lb':
            if 40 <= data['weight'] <= 300:
                weight = WeightMeasurement(lb=data['weight'])
            else:
                raise serializers.ValidationError('Weight %s lb seems to be wrong.' % data['weight'])
        else:
            raise serializers.ValidationError('Field unit needs to be kg or lb!')
        data.pop('unit')
        data['weight'] = weight
        return data

    def to_representation(self, instance):
        weight = instance.value_club_unit()[0]
        unit = instance.value_club_unit()[1]
        return {
            'weight': weight,
            'unit': unit,
            'date': instance.date,
            'player': instance.player.id
        }


class ParentsHeightSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(allow_blank=False, max_length=10, required=True)

    class Meta:
        model = ParentsHeight
        fields = ('player', 'fathers_height', 'mothers_height', 'unit')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if data['unit'] == 'cm':
            if (50 <= data['fathers_height'] <= 250) and (50 <= data['mothers_height'] <= 250):
                fathers_height = Distance(cm=data['fathers_height'])
                mothers_height = Distance(cm=data['mothers_height'])
            else:
                raise serializers.ValidationError('Height (%s / %s) cm seems to be wrong.' % (data['fathers_height'],
                                                                                              data['mothers_height']))
        elif data['unit'] == 'inch':
            if (20 <= data['fathers_height'] <= 100) and (20 <= data['mothers_height'] <= 100):
                fathers_height = Distance(inch=data['fathers_height'])
                mothers_height = Distance(inch=data['mothers_height'])
            else:
                raise serializers.ValidationError('Height (%s / %s) inch seems to be wrong.' % (data['fathers_height'],
                                                                                                data['mothers_height']))
        else:
            raise serializers.ValidationError('Field unit needs to be cm or inch!')
        data.pop('unit')
        data['fathers_height'] = fathers_height
        data['mothers_height'] = mothers_height
        return data

    def to_representation(self, instance):
        fathers_height = instance.value_club_unit()[0]
        mothers_height = instance.value_club_unit()[1]
        unit = instance.value_club_unit()[2]
        return {
            'fathers_height': fathers_height,
            'mothers_height': mothers_height,
            'unit': unit,
            'player': instance.player.id
        }


class SittingHeightSerializer(serializers.ModelSerializer):
    unit = serializers.CharField(allow_blank=False, max_length=10, required=True)

    class Meta:
        model = SittingHeight
        fields = ('player', 'date', 'sitting_height', 'unit')

    def validate(self, data):
        group = self.context['request'].user.groups.values_list('name', flat=True)

        if 'Club' in group:
            if data['player'].club != self.context['request'].user.club:
                raise exceptions.PermissionDenied('Club has no permission to access performance data of player.')
        elif 'Coach' in group:
            if data['player'].club != self.context['request'].user.coach.club:
                raise exceptions.PermissionDenied('Coach has no permission to access performance data of player.')
        elif 'Player' in group:
            raise exceptions.PermissionDenied('Players can not post performance data.')
        else:
            raise exceptions.PermissionDenied('User group not selected.')

        if data['unit'] == 'cm':
            if 50 <= data['sitting_height'] <= 250:
                sitting_height = Distance(cm=data['sitting_height'])
            else:
                raise serializers.ValidationError('Height %s cm seems to be wrong.' % data['sitting_height'])
        elif data['unit'] == 'inch':
            if 20 <= data['height'] <= 100:
                sitting_height = Distance(inch=data['height'])
            else:
                raise serializers.ValidationError('Height %s inch seems to be wrong.' % data['sitting_height'])
        else:
            raise serializers.ValidationError('Field unit needs to be cm or inch!')
        data.pop('unit')
        data['sitting_height'] = sitting_height
        return data

    def to_representation(self, instance):
        sitting_height = instance.value_club_unit()[0]
        unit = instance.value_club_unit()[1]
        return {
            'sitting_height': sitting_height,
            'unit': unit,
            'date': instance.date,
            'player': instance.player.id
        }
