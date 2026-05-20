from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.URLField(max_length=2083, blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        active_offer = self.offers.first()
        if active_offer:
            # Performs precise decimal reduction calculations
            return self.price - (self.price * (active_offer.discount / 100))
        return self.price


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)

    discount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.code} ({self.discount}% OFF)"