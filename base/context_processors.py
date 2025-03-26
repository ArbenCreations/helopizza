import asyncio
import json
import logging
from django.core.cache import cache
import httpx

logger = logging.getLogger(__name__)

API_URL = "https://api.utellorders.ca/api/v1/products/all_products"
VENDOR_ID = "12"
CATEGORIES_CACHE_KEY = "categories_cache"
PRODUCTS_CACHE_KEY = "products_cache"
CACHE_TIMEOUT = 1800  # 30 minutes


async def fetch_menu():
    """Fetch menu products from external API asynchronously."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                API_URL,
                headers={"Content-Type": "application/json"},
                json={"vendor_id": VENDOR_ID, "page_number": 1, "page_size": 100},
            )
            response.raise_for_status()
            return response.json()  # Assuming API returns JSON
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch menu: {e}")
        return None


async def fetch_cats():
    """Fetch menu categories from external API asynchronously."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(
                f"https://api.utellorders.ca/api/v1/products/{VENDOR_ID}/get_product_categories",
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()  # Assuming API returns JSON
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch categories: {e}")
        return None


async def async_categories_processor():
    """Asynchronous Django context processor with caching."""
    categories = cache.get(CATEGORIES_CACHE_KEY)
    products = cache.get(PRODUCTS_CACHE_KEY)

    tasks = []
    if not categories:
        tasks.append(fetch_cats())
    if not products:
        tasks.append(fetch_menu())

    if tasks:
        results = await asyncio.gather(*tasks)  # Run API calls in parallel

        if not categories and results[0]:
            categories = results[0].get("data", [])
            cache.set(CATEGORIES_CACHE_KEY, categories, CACHE_TIMEOUT)

        if not products and len(results) > 1 and results[1]:
            products = results[1].get("data", [])
            cache.set(PRODUCTS_CACHE_KEY, products, CACHE_TIMEOUT)

    return {"categories": categories or [], "products": products or []}


def categories_processor(request):
    """Wrapper for async function to make it work in Django."""
    return asyncio.run(async_categories_processor())  # Blocking call to run async function
