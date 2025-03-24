from .models import Category
import requests
import json
import logging

logger = logging.getLogger(__name__)


API_URL = "https://api.utellorders.ca/api/v1/products/all_products"
VENDOR_ID = "12"

def fetch_menu():
    """Fetch menu categories from external API."""
    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"vendor_id": VENDOR_ID, "page_number": 1, "page_size": 100}),
            timeout=5  # Avoid hanging requests
        )
        response.raise_for_status()
        print(response.json())
        return response.json() # Assuming the API returns JSON
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu: {e}")
        return None
    
def fetch_cats():
    """Fetch menu categories from external API."""
    try:
        response = requests.get(
            'https://api.utellorders.ca/api/v1/products/12/get_product_categories',
            headers={"Content-Type": "application/json"},
            timeout=5  # Avoid hanging requests
        )
        response.raise_for_status()
        print(response.json())
        return response.json() # Assuming the API returns JSON
    except requests.RequestException as e:
        logger.error(f"Failed to fetch menu: {e}")
        return None
def categories_processor(request):
    # categories = Category.objects.all()
    categories =fetch_cats()['data']
    products=fetch_menu()
    return {'categories': categories,'products':products['data']}