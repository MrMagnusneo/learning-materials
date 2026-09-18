#from progress.bar import IncrementalBar
import time
import math
from tqdm import tqdm
import rolimons
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd


# Fetches statistics for Valkyrie Helm
item = rolimons.item(193811031)
#print(f"item rap:{item.rap} item value:{item.value}")

# Gets sales data for Valkyrie Helm
sales = item.get_recent_sales()

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    min_samples_leaf=3
)

#bar = IncrementalBar('Collecting', max = len(sales))

rows = []

for sale in tqdm(sales):
    #bar.next()
    rows.append({
        "timestamp": sale.timestamp,
        "price": sale.sales_price,
        "old_rap": sale.old_rap,
        "new_rap": sale.new_rap,
        "item_rap": item.rap,
        "item_value": item.value,
        "item_default_value": item.default_value,
        "item_demand": item.demand,
        "item_trend": item.trend,
        "item_projected": int(item.projected),
        "item_hyped": int(item.hyped),
        "item_rare": int(item.rare),
    })

df = pd.DataFrame(rows).sort_values("timestamp")
df["prev_price"] = df["price"].shift(1)
df["prev_old_rap"] = df["old_rap"].shift(1)
df["prev_new_rap"] = df["new_rap"].shift(1)
df["time_since_prev_sale"] = df["timestamp"] - df["timestamp"].shift(1)

df_sales = df.dropna(subset=[
    "price",
    "old_rap",
    "prev_price",
    "prev_new_rap",
    "time_since_prev_sale",
])

X = df_sales[[
    "timestamp",
    "item_rap",
    "item_value",
    "item_default_value",
    "item_demand",
    "item_trend",
    "item_projected",
    "item_hyped",
    "item_rare",
    "prev_price",
    "prev_old_rap",
    "prev_new_rap",
    "time_since_prev_sale",
]]
y = df_sales["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

print(f"\nCollected data:\n{df}")
print(f"\nTraining rows: {len(X_train)}")
print(f"Testing rows: {len(X_test)}")
#print(f"sale timestamp:{sale.timestamp} sale old_rap:{sale.old_rap} sale new_rap:{sale.new_rap} sale sales_price:{sale.sales_price}")


model.fit(X_train, y_train)

predictions = model.predict(X_test)

result = pd.DataFrame({
    "real_price": y_test,
    "predicted_price": predictions,
})

print(result)