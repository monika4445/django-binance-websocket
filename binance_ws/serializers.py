from rest_framework import serializers
from .models import CryptoPrice

class CryptoPriceSerializer(serializers.ModelSerializer):
    formatted_timestamp = serializers.DateTimeField(source='timestamp', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = CryptoPrice
        fields = ['pair_name', 'price', 'formatted_timestamp']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
