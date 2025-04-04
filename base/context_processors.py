import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
import httpx

logger = logging.getLogger(__name__)

API_URL = "https://api.utellorders.ca/api/v1/products/all_products"
VENDOR_ID = "12"
Banner_url='https://api.utellorders.ca/api/v1/banner_settings/banner_list'
# File paths for storing data locally
DATA_DIR = "data_store"
BANNERS_FILE = os.path.join(DATA_DIR, "banner.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

# Expiry time (30 minutes)
CACHE_TIMEOUT = timedelta(minutes=30)


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
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch menu: {e}")
        return None


async def fetch_banner():
    """Fetch Banner  from external API asynchronously."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                Banner_url,
                headers={"Content-Type": "application/json"},
                json={"vendor_id": VENDOR_ID, "page_number": 1, "page_size": 100},
            )
            response.raise_for_status()
            return response.json()
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
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"Failed to fetch categories: {e}")
        return None


def save_to_file(filepath, data):
    """Save data to a local JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.utcnow().isoformat(), "data": data}, f)


def load_from_file(filepath):
    """Load data from a local JSON file if not expired."""
    if not os.path.exists(filepath):
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)
            timestamp = datetime.fromisoformat(content["timestamp"])
            if datetime.utcnow() - timestamp < CACHE_TIMEOUT:
                return content["data"]  # Return cached data if still valid
    except (json.JSONDecodeError, KeyError):
        return None  # Return None if file is corrupt or missing data

    return None


async def update_local_data():
    """Fetch latest data and save it to local files."""
    categories, products, banners = ["","",""]

    if banners:
        save_to_file(BANNERS_FILE, banners.get("data", []))

    if categories:
        save_to_file(CATEGORIES_FILE, categories.get("data", []))

    if products:
        save_to_file(PRODUCTS_FILE, products.get("data", []))


def categories_processor(request):
    """Load data from local file, triggering background update if necessary."""
    categories = load_from_file(CATEGORIES_FILE)
    products = load_from_file(PRODUCTS_FILE)
    Banners=load_from_file(BANNERS_FILE)

    if categories is None or products is None or Banners is None:
        asyncio.run(update_local_data())  # Trigger background update

    return {"categories": categories or [], "products": products or [],"Banners":Banners or []}
async def preload_data():
    await update_local_data()

# asyncio.run(preload_data())  # Run this once on startup