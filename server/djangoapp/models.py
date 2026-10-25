from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    BODY_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('Hatchback', 'Hatchback'),
        ('Coupe', 'Coupe'),
        ('Minivan', 'Minivan'),
        ('Truck', 'Truck'),
        ('Other', 'Other'),
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, default='Sedan')
    year = models.IntegerField(default=2023, validators=[MinValueValidator(2015), MaxValueValidator(2023)])
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['make__name', 'name']
        constraints = [models.UniqueConstraint(fields=['make', 'name', 'year'], name='unique_carmodel_per_make_year')]

    def __str__(self):
        return f'{self.make.name} {self.name} ({self.year})'


class Dealer(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=10, blank=True, default='')
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10, db_column='zip')
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    short_name = models.CharField(max_length=100, blank=True, default='')
    full_name = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.full_name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])
    sentiment = models.CharField(max_length=20, default='neutral')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.dealership.full_name}'
