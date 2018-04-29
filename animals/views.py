from datetime import datetime, timedelta

from django.db.models import Avg
from rest_framework import generics, status
from rest_framework.response import Response

from animals.models import Animal, AnimalWeight
from animals.serializers import AnimalSerializer, AnimalWeightSerializer


def convert_date_inverse(s):
    """
        Convert date
    """
    try:
        return datetime(int(s[:4]), int(s[5:7]), int(s[-2:]))
    except Exception:
        return datetime.now()


class AnimalList(generics.ListCreateAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    name = 'animal-list'


class AnimalDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    name = 'animal-detail'


class AnimalWeightList(generics.ListCreateAPIView):

    queryset = AnimalWeight.objects.all()
    serializer_class = AnimalWeightSerializer
    name = 'animalweight-list'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        animal_weight = AnimalWeight.objects.create(animal_id=int(kwargs['animal']),
                                                    weight=request.data['weight'],
                                                    weight_date=request.data['weight_date'])

        result = AnimalWeightSerializer(animal_weight)

        return Response(result.data, status=status.HTTP_201_CREATED)


class AnimalWeightDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = AnimalWeight.objects.all()
    serializer_class = AnimalWeightSerializer
    name = 'animalweight-detail'


class AnimalEstimatedWeightList(generics.ListCreateAPIView):

    name = 'animal-estimatedweight-list'

    def get(self, request, *args, **kwargs):

        if 'date' in request.GET and request.GET['date']:
            date_param = convert_date_inverse(request.GET['date'].split('T')[0]).date()

            # amount of animals
            num_animals = Animal.objects.count()

            # list of animals weight
            animals_weights_list = AnimalWeight.objects.all()

            # average of weights
            animals_weights_average = animals_weights_list.aggregate(avg=Avg('weight'))['avg']

            # inits values
            first_aw_by_date = animals_weights_list.order_by('weight_date')[0]
            last_aw_by_date = animals_weights_list.order_by('-weight_date')[0]

            # init dates
            initial_date = first_aw_by_date.weight_date
            end_date = last_aw_by_date.weight_date

            # init and end weight values
            initial_weight = first_aw_by_date.weight
            end_weight = last_aw_by_date.weight

            # amount of days
            days = (end_date - initial_date).days

            # average for days
            average_date_days = days / 2

            # average date
            average_date = initial_date + timedelta(days=average_date_days)

            # weights per day
            animals_weights_per_day = (last_aw_by_date.weight - first_aw_by_date.weight) / days

            estimated_total_weight = 0

            if initial_date.date() <= date_param <= end_date.date():

                if date_param == average_date.date():
                    estimated_total_weight = animals_weights_average
                else:
                    # inter
                    increment_days = (date_param - initial_date.date()).days
                    estimated_total_weight = initial_weight + (animals_weights_per_day * increment_days)

            if date_param > end_date.date():

                # extra
                increment_days = (date_param - end_date.date()).days
                estimated_total_weight = end_weight + (animals_weights_per_day * increment_days)

            return Response({'num_animals': num_animals,
                             'estimated_total_weight': estimated_total_weight}, status=status.HTTP_200_OK)

        return Response({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
