"""
Generates a synthetic but structurally realistic monthly inventory dataset:
Category x Season x Month, with units sold, units in stock, price, discount.
Same transparency note as the Python project: synthetic data, real structure,
built because live scraped data isn't reachable from this sandbox.
"""
import random
import csv

random.seed(7)

CATEGORIES = ["T-Shirt", "Jeans", "Dress", "Jacket", "Kurta", "Sneakers"]
SEASON_MONTHS = {
    "Summer": ["Mar", "Apr", "May", "Jun"],
    "Monsoon": ["Jul", "Aug", "Sep"],
    "Winter": ["Oct", "Nov", "Dec", "Jan"],
    "Spring": ["Feb"],
}

BASE_PRICE = {
    "T-Shirt": 699, "Jeans": 1699, "Dress": 1499,
    "Jacket": 2499, "Kurta": 1199, "Sneakers": 2999,
}

rows = []
sku_counter = 1
for season, months in SEASON_MONTHS.items():
    for category in CATEGORIES:
        for month in months:
            sku = f"SKU-{category[:2].upper()}{sku_counter:04d}"
            sku_counter += 1
            # Seasonal demand multiplier makes the trend meaningful
            if (season == "Summer" and category in ["T-Shirt", "Dress"]) or \
               (season == "Winter" and category in ["Jacket", "Kurta"]) or \
               (season == "Monsoon" and category in ["Sneakers"]):
                demand_mult = random.uniform(1.4, 2.2)
            else:
                demand_mult = random.uniform(0.5, 1.1)

            units_sold = int(random.uniform(40, 160) * demand_mult)
            units_in_stock = int(units_sold * random.uniform(0.3, 1.2))
            price = round(BASE_PRICE[category] * random.uniform(0.9, 1.15), 2)
            discount = random.choice([0, 10, 15, 20, 30, 40])

            rows.append([sku, category, season, month, units_sold, units_in_stock, price, discount])

with open("raw_inventory.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["SKU", "Category", "Season", "Month", "Units_Sold",
                      "Units_In_Stock", "Price_INR", "Discount_Pct"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> raw_inventory.csv")
