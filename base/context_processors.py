# import json
# import logging
# import os
# from datetime import datetime, timedelta
# import requests

# logger = logging.getLogger(__name__)

# API_URL = "https://api.utellorders.ca/api/v1/products/all_products"
# VENDOR_ID = "12"
# BANNER_URL = "https://api.utellorders.ca/api/v1/banner_settings/banner_list"

# # File paths for storing data locally
# DATA_DIR = "data_store"
# BANNERS_FILE = os.path.join(DATA_DIR, "banner.json")
# CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
# PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

# # Expiry time (30 minutes)
# CACHE_TIMEOUT = timedelta(minutes=30)


# def fetch_menu():
#     """Fetch menu products from external API."""
#     try:
#         response = requests.post(
#             API_URL,
#             headers={"Content-Type": "application/json"},
#             json={"vendor_id": VENDOR_ID, "page_number": 1, "page_size": 100},
#             timeout=5,
#         )
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         logger.error(f"Failed to fetch menu: {e}")
#         return None


# def fetch_banner():
#     """Fetch banner from external API."""
#     try:
#         response = requests.post(
#             BANNER_URL,
#             headers={"Content-Type": "application/json"},
#             json={"vendor_id": VENDOR_ID, "page_number": 1, "page_size": 100},
#             timeout=5,
#         )
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         logger.error(f"Failed to fetch banner: {e}")
#         return None


# def fetch_cats():
#     """Fetch menu categories from external API."""
#     try:
#         response = requests.get(
#             f"https://api.utellorders.ca/api/v1/products/{VENDOR_ID}/get_product_categories",
#             headers={"Content-Type": "application/json"},
#             timeout=5,
#         )
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         logger.error(f"Failed to fetch categories: {e}")
#         return None


# def save_to_file(filepath, data):
#     """Save data to a local JSON file."""
#     os.makedirs(DATA_DIR, exist_ok=True)
#     with open(filepath, "w", encoding="utf-8") as f:
#         json.dump({"timestamp": datetime.utcnow().isoformat(), "data": data}, f)


# def load_from_file(filepath):
#     """Load data from a local JSON file if not expired."""
#     if not os.path.exists(filepath):
#         return None

#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             content = json.load(f)
#             timestamp = datetime.fromisoformat(content["timestamp"])
#             if datetime.utcnow() - timestamp < CACHE_TIMEOUT:
#                 return content["data"]
#     except (json.JSONDecodeError, KeyError):
#         return None

#     return None


# def update_local_data():
#     """Fetch latest data and save it to local files."""
#     banners = fetch_banner()
#     categories = fetch_cats()
#     products = fetch_menu()

#     if banners:
#         save_to_file(BANNERS_FILE, banners.get("data", []))

#     if categories:
#         save_to_file(CATEGORIES_FILE, categories.get("data", []))

#     if products:
#         save_to_file(PRODUCTS_FILE, products.get("data", []))


# def categories_processor(request):
#     """Load data from local file, trigger update if necessary."""
#     categories = load_from_file(CATEGORIES_FILE)
#     products = load_from_file(PRODUCTS_FILE)
#     banners = load_from_file(BANNERS_FILE)

#     if categories is None or products is None or banners is None:
#         update_local_data()

#     return {
#         "categories": categories or [],
#         "products": products or [],
#         "Banners": banners or [],
#     }


# # def preload_data_sync():
# #     """Manually trigger data preload at startup."""
# #     update_local_data()
# # preload_data_sync()