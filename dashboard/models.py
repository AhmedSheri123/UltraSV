from django.db import models
from .countrys import list_of_countrys
# Create your models here.

class VisitPriceByCountry(models.Model):
    country = models.CharField(choices=list_of_countrys, max_length=250, verbose_name='الدولة')
    price_per_one_visit = models.DecimalField(max_digits=6, decimal_places=3, verbose_name='سعر لكل زيارة')

    def __str__(self):
        return self.country
    class Meta:
        ordering = ['-price_per_one_visit']

    def getCountryNmae(self):
        for country_code in list_of_countrys:
            if self.country == country_code[0]:
                return country_code[1]