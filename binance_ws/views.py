from .models import CryptoPrice
from .serializers import CryptoPriceSerializer
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

class CryptoPriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CryptoPrice.objects.all().order_by('-timestamp')  # Get all prices ordered by timestamp
    serializer_class = CryptoPriceSerializer


class CryptoPriceHistory(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch all prices ordered by timestamp
        queryset = CryptoPrice.objects.all().order_by('-timestamp')

        # Paginate the queryset
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Optional: You can customize page size here
        result_page = paginator.paginate_queryset(queryset, request)

        # Serialize the paginated data
        serializer = CryptoPriceSerializer(result_page, many=True)

        # Return the paginated response
        return paginator.get_paginated_response(serializer.data)
