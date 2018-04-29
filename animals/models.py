from django.db import models


class Animal(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return '{}'.format(self.id)

    def get_my_weights(self):
        return self.weights.all()


class AnimalWeight(models.Model):
    animal = models.ForeignKey(Animal, related_name='weights', on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    weight_date = models.DateTimeField()

    class Meta:
        ordering = ('animal', 'weight_date')

    def __str__(self):
        return '{} (W: {}, D: {})'.format(self.animal, self.weight, self.weight_date.strftime("%m-%d-%Y"))
