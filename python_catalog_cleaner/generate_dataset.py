"""
generate_dataset.py
--------------------
Generates a SYNTHETIC fashion e-commerce catalog dataset (1,200 rows) that mimics
the structure of real marketplace exports (e.g. Myntra/Ajio/Amazon Fashion listings).

Why synthetic: this sandbox has no live internet access, so a real Kaggle/scraped
dataset can't be downloaded here. The structure, value ranges, and messiness
(missing values, duplicate rows, inconsistent casing, stray whitespace) are modeled
on real fashion catalog exports so the cleaning script solves a genuine problem.

Be transparent about this if asked in an interview: "I generated a structurally
realistic dataset to build and test the pipeline, since I didn't have access to a
live scraped dataset at the time."
"""

import random
import csv

random.seed(42)

BRANDS = ["Urbanic", "H&M", "Zara", "Roadster", "Levis", "Puma", "Bewakoof",
          "Only", "Vero Moda", "Mango", "AND", "Forever 21", "Nike", "Adidas", "Biba"]

CATEGORIES = ["T-Shirt", "Jeans", "Dress", "Jacket", "Kurta", "Sneakers",
              "Hoodie", "Skirt", "Formal Shirt", "Co-ord Set"]

COLORS = ["Black", "White", "Beige", "Olive", "Pink", "Blue", "Red", "Grey", "Yellow", "Maroon"]

SEASONS = ["Summer", "Winter", "Monsoon", "All-Season"]

rows = []
for i in range(1, 1201):
    brand = random.choice(BRANDS)
    category = random.choice(CATEGORIES)
    color = random.choice(COLORS)
    season = random.choice(SEASONS)
    price = round(random.uniform(399, 4999), 2)
    discount_pct = random.choice([0, 10, 20, 30, 40, 50, 60])
    rating = round(random.uniform(2.5, 5.0), 1)
    num_ratings = random.randint(0, 5000)

    # Inject realistic messiness
    if random.random() < 0.05:
        price = ""  # missing price
    if random.random() < 0.04:
        rating = ""  # missing rating
    if random.random() < 0.06:
        brand = brand.upper() if random.random() < 0.5 else brand.lower()  # inconsistent casing
    if random.random() < 0.03:
        category = f"  {category} "  # stray whitespace

    rows.append([
        f"SKU{1000+i}", brand, category, color, season,
        price, discount_pct, rating, num_ratings
    ])

# Inject ~30 duplicate rows (common in scraped/merged catalog exports)
for _ in range(30):
    rows.append(random.choice(rows[:1200]))

random.shuffle(rows)

with open("fashion_catalog_raw.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["sku_id", "brand", "category", "color", "season",
                      "price_inr", "discount_pct", "rating", "num_ratings"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows -> fashion_catalog_raw.csv")
