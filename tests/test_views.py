import pytest
from rest_framework.test import APIClient
from binance_ws.models import CryptoPrice

@pytest.mark.django_db
def test_get_price_history():
    # Create some data
    CryptoPrice.objects.create(pair_name="BTC/USDT", price=30000)
    CryptoPrice.objects.create(pair_name="ETH/USDT", price=2000)

    # Instantiate the APIClient
    client = APIClient()

    # Send GET request to your price history endpoint
    response = client.get('/api/history/')

    # Check if the status code is correct (200 OK)
    assert response.status_code == 200

    # Check the response data
    data = response.json()
    assert 'results' in data  # Change 'prices' to 'results' (based on pagination response)
    assert len(data['results']) > 0
    assert "pair_name" in data['results'][0]
    assert "price" in data['results'][0]

@pytest.mark.django_db
def test_prices_viewset():
    # Create some data
    CryptoPrice.objects.create(pair_name="BTC/USDT", price=30000)
    CryptoPrice.objects.create(pair_name="ETH/USDT", price=2000)

    # Instantiate the APIClient
    client = APIClient()

    # Send GET request to the price list endpoint
    response = client.get('/api/prices/')

    # Print the response to inspect its structure
    print(response.json())

    # Check if the status code is correct (200 OK)
    assert response.status_code == 200

    # Check if the response data contains the expected fields
    data = response.json()
    assert isinstance(data['results'], list)  # Make sure 'results' is a list
    assert len(data['results']) > 0  # Ensure the data is not empty
    assert "pair_name" in data['results'][0]  # Ensure the pair_name field exists in the response
    assert "price" in data['results'][0]  # Ensure the price field exists in the response



