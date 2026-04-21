import pandas as pd
import requests
from datetime import datetime, timedelta
import random


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
DUMMYJSON_CARTS_URL  = "https://dummyjson.com/carts?limit=100"
DUMMYJSON_PRODUCTS_URL = "https://dummyjson.com/products?limit=100"
FALLBACK_CSV         = "data/sales_data.csv"

REGIONS   = ["East", "West", "Central", "South"]
DATE_RANGE_DAYS = 365   # spread synthetic order dates across the past year


# ─────────────────────────────────────────────
# DATA FETCHING
# ─────────────────────────────────────────────

def fetch_data() -> pd.DataFrame:
    """
    Primary: pull live cart + product data from DummyJSON and
    return a DataFrame that matches the pipeline's expected schema:
        Order Date | Region | Category | Sub-Category | Sales | Profit | Quantity

    Fallback: if the API is unreachable, load from the local CSV.
    """
    try:
        print("   → Requesting cart data from DummyJSON...")
        carts_resp    = requests.get(DUMMYJSON_CARTS_URL,    timeout=10)
        products_resp = requests.get(DUMMYJSON_PRODUCTS_URL, timeout=10)

        carts_resp.raise_for_status()
        products_resp.raise_for_status()

        carts    = carts_resp.json()["carts"]
        products = {p["id"]: p for p in products_resp.json()["products"]}

        df = _build_dataframe(carts, products)
        print(f"   → Live data loaded: {len(df)} order lines from DummyJSON ✅")
        return df

    except Exception as e:
        print(f"   ⚠️  API unavailable ({e}). Falling back to local CSV...")
        df = pd.read_csv(FALLBACK_CSV)
        print(f"   → CSV loaded: {len(df)} records ✅")
        return df


def _build_dataframe(carts: list, products: dict) -> pd.DataFrame:
    """
    Flatten DummyJSON carts into one row per cart-item, enriched with
    product metadata, synthetic dates, regions, and estimated profit.
    """
    random.seed(42)   # reproducible output across runs
    base_date = datetime.today()
    rows = []

    for cart in carts:
        # Spread orders evenly across the past year
        days_ago   = random.randint(0, DATE_RANGE_DAYS)
        order_date = (base_date - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        region     = random.choice(REGIONS)

        for item in cart.get("products", []):
            product = products.get(item["id"])
            if not product:
                continue

            category     = product.get("category", "Uncategorized").title()
            sub_category = product.get("title", "Unknown")[:30]   # trim long names
            price        = item.get("price", product.get("price", 0))
            quantity     = item.get("quantity", 1)
            sales        = round(price * quantity, 2)
            # DummyJSON doesn't have profit; estimate from discountPercentage
            discount     = product.get("discountPercentage", 10) / 100
            profit       = round(sales * discount * random.uniform(0.8, 1.2), 2)

            rows.append({
                "Order Date":   order_date,
                "Region":       region,
                "Category":     category,
                "Sub-Category": sub_category,
                "Sales":        sales,
                "Profit":       profit,
                "Quantity":     quantity,
            })

    df = pd.DataFrame(rows)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df = df.sort_values("Order Date").reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────

def analyze(df: pd.DataFrame) -> dict:
    """Run key sales analysis and return a summary dict."""
    summary = {}

    # Overall revenue
    summary["total_revenue"]       = round(df["Sales"].sum(), 2)
    summary["average_order_value"] = round(df["Sales"].mean(), 2)
    summary["total_orders"]        = len(df)

    # Top 5 categories by revenue
    top_products = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
    )
    summary["top_products"] = top_products.to_dict()

    # Revenue by region
    region_revenue = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )
    summary["revenue_by_region"] = region_revenue.to_dict()

    # Monthly trend — last 6 months
    df = df.copy()
    df["Month"] = pd.to_datetime(df["Order Date"]).dt.to_period("M")
    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .tail(6)
        .round(2)
    )
    summary["last_6_months"] = {str(k): v for k, v in monthly.to_dict().items()}

    return summary