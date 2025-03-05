from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from binance_ws.views import CryptoPriceViewSet, CryptoPriceHistory

router = DefaultRouter()
router.register(r'prices', CryptoPriceViewSet, basename='prices')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/history/', CryptoPriceHistory.as_view(), name='price-history'),
]

