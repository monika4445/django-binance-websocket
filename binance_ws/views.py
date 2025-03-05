from rest_framework import viewsets
from .models import CryptoPrice
from .serializers import CryptoPriceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CryptoPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CryptoPrice.objects.all().order_by('-timestamp')
    serializer_class = CryptoPriceSerializer

class CryptoPriceHistory(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch last 10 prices (can be changed as needed)
        prices = CryptoPrice.objects.all().order_by('-timestamp')[:10]
        return Response({
            "prices": [{"pair": price.pair_name, "price": price.price} for price in prices]
        })



