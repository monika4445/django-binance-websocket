from django.db import models

class CryptoPrice(models.Model):
    pair_name = models.CharField(max_length=20)  # Can be BTC/USDT or any other pair
    price = models.DecimalField(max_digits=20, decimal_places=8)  # Price of the cryptocurrency
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of when the price was received

    def __str__(self):
        return f'{self.pair_name} - {self.price} at {self.timestamp}'
