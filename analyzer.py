import pandas as pd
import requests
import io

def fetch_data():
    """Load local sales dataset"""
    df = pd.read_csv("data/sales_data.csv")
    return df

def analyze(df):
    """Run key sales analysis and return a summary dict"""
    summary = {}

    # Overall revenue
    summary["total_revenue"] = round(df["Sales"].sum(), 2)
    summary["average_order_value"] = round(df["Sales"].mean(), 2)
    summary["total_orders"] = len(df)

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

    # Monthly trend - last 6 months
    df["Month"] = pd.to_datetime(df["Order Date"]).dt.to_period("M")
    monthly = (
        df.groupby("Month")["Sales"]
        .sum()
        .tail(6)
        .round(2)
    )
    summary["last_6_months"] = {str(k): v for k, v in monthly.to_dict().items()}

    return summary