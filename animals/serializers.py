from rest_framework import serializers

from animals.models import Animal, AnimalWeight


class AnimalSerializer(serializers.ModelSerializer):

    weights = serializers.SerializerMethodField()

    class Meta:
        model = Animal
        fields = ('id', 'weights')

    def get_weights(self, obj):
        return [AnimalWeightSerializer(x).data for x in obj.get_my_weights()]


class AnimalWeightSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalWeight
        fields = ('id', 'weight', 'weight_date')
