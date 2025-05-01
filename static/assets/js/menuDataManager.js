const API_URL = "https://api.utellorders.ca/api/v1/products/all_products";
const VENDOR_ID = "12";
const BANNER_URL = "https://api.utellorders.ca/api/v1/banner_settings/banner_list";
const CATEGORIES_URL = `https://api.utellorders.ca/api/v1/products/${VENDOR_ID}/get_product_categories`;
const CACHE_TIMEOUT = 30 * 60 * 1000; // 30 minutes in milliseconds

function saveToStorage(key, data) {
  const payload = {
    timestamp: new Date().toISOString(),
    data: data,
  };
  localStorage.setItem(key, JSON.stringify(payload));
}

function loadFromStorage(key) {
  const raw = localStorage.getItem(key);
  if (!raw) return null;

  try {
    const parsed = JSON.parse(raw);
    const savedTime = new Date(parsed.timestamp);
    const now = new Date();
    if (now - savedTime < CACHE_TIMEOUT) {
      return parsed.data;
    }
  } catch (e) {
    console.error(`Failed to parse cache for ${key}:`, e);
  }

  return null;
}

async function fetchAPI(url, method = "GET", body = null) {
  try {
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : null,
    });

    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const json = await response.json();
    return json.data || [];
  } catch (e) {
    console.error(`Error fetching ${url}:`, e);
    return null;
  }
}

async function updateLocalData() {
  const [banners, categories, products] = await Promise.all([
    fetchAPI(BANNER_URL, "POST", { vendor_id: VENDOR_ID, page_number: 1, page_size: 100 }),
    fetchAPI(CATEGORIES_URL, "GET"),
    fetchAPI(API_URL, "POST", { vendor_id: VENDOR_ID, page_number: 1, page_size: 100 }),
  ]);

  if (banners) saveToStorage("banners", banners);
  if (categories) saveToStorage("categories", categories);
  if (products) saveToStorage("products", products);
}

async function getMenuData() {
  let categories = loadFromStorage("categories");
  let products = loadFromStorage("products");
  let banners = loadFromStorage("banners");

  if (!categories || !products || !banners) {
    await updateLocalData();
    categories = loadFromStorage("categories");
    products = loadFromStorage("products");
    banners = loadFromStorage("banners");
  }

  return {
    categories: categories || [],
    products: products || [],
    banners: banners || [],
  };
}

// Trigger preload on page load
getMenuData().then(data => {
  console.log("Preloaded data:", data);
});
