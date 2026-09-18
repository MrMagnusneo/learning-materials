import requests
import pandas as pd

def get_resale_data(asset_id):
    url = f"https://economy.roblox.com/v1/assets/{asset_id}/resale-data"
    data = requests.get(url).json()

    prices = pd.DataFrame(data["priceDataPoints"])
    volumes = pd.DataFrame(data["volumeDataPoints"])

    prices = prices.rename(columns={"value": "avg_resale_price"})
    volumes = volumes.rename(columns={"value": "sales_volume"})

    df = prices.merge(volumes, on="date", how="outer")
    df["date"] = pd.to_datetime(df["date"])
    df["asset_id"] = asset_id

    df["recent_average_price"] = data.get("recentAveragePrice")
    df["total_sales"] = data.get("sales")
    df["original_price"] = data.get("originalPrice")
    df["asset_stock"] = data.get("assetStock")
    df["number_remaining"] = data.get("numberRemaining")

    return df.sort_values("date")

resale_df = get_resale_data(1365767)
print(resale_df)