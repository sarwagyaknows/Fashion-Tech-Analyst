"""
clean_catalog.py
-----------------
Fashion Tech Analyst Project 1: Catalog Cleaning & Ranking Engine

Takes a raw, messy fashion catalog export (fashion_catalog_raw.csv — 1,230 rows)
and produces a clean, de-duplicated, ranked catalog ready for merchandising review.

Deliberately uses only basic Python constructs (loops, dicts, lists) rather than
pandas one-liners, to demonstrate manual control over each cleaning step —
useful when explaining exactly what happened to a non-technical stakeholder.

Cleaning steps:
  1. Strip whitespace, normalize casing (brand/category/color/season)
  2. Drop rows with missing price or rating (can't rank incomplete listings)
  3. Remove duplicate SKUs (keep first occurrence)
  4. Compute discounted (effective) price for each item
  5. Filter: keep items priced under 5000 INR with rating >= 3.5
  6. Sort by a composite "deal score" (high rating, high discount, low price)
  7. Write cleaned_catalog.csv + print a merchandising summary
"""

import csv

INPUT_FILE = "fashion_catalog_raw.csv"
OUTPUT_FILE = "cleaned_catalog.csv"

PRICE_CEILING = 5000
MIN_RATING = 3.5


def load_raw_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def clean_row(row):
    """Return a cleaned dict, or None if the row should be dropped."""
    sku = row["sku_id"].strip()
    brand = row["brand"].strip().title()
    category = row["category"].strip().title()
    color = row["color"].strip().title()
    season = row["season"].strip().title()

    price_raw = row["price_inr"].strip()
    rating_raw = row["rating"].strip()

    if price_raw == "" or rating_raw == "":
        return None  # incomplete listing, can't be ranked reliably

    try:
        price = float(price_raw)
        rating = float(rating_raw)
        discount_pct = float(row["discount_pct"])
        num_ratings = int(row["num_ratings"])
    except ValueError:
        return None  # corrupted numeric field

    return {
        "sku_id": sku,
        "brand": brand,
        "category": category,
        "color": color,
        "season": season,
        "price_inr": round(price, 2),
        "discount_pct": discount_pct,
        "rating": rating,
        "num_ratings": num_ratings,
    }


def deduplicate(rows):
    seen_skus = set()
    unique_rows = []
    duplicates_removed = 0
    for row in rows:
        if row["sku_id"] in seen_skus:
            duplicates_removed += 1
            continue
        seen_skus.add(row["sku_id"])
        unique_rows.append(row)
    return unique_rows, duplicates_removed


def add_derived_fields(rows):
    for row in rows:
        effective_price = row["price_inr"] * (1 - row["discount_pct"] / 100)
        row["effective_price_inr"] = round(effective_price, 2)
        # Deal score: reward high rating + high discount, penalize high price.
        # Weighted manually (rating matters most, then discount, then price).
        row["deal_score"] = round(
            (row["rating"] * 20) + (row["discount_pct"] * 0.5) - (effective_price / 100),
            2
        )
    return rows


def filter_catalog(rows):
    filtered = []
    for row in rows:
        if row["effective_price_inr"] <= PRICE_CEILING and row["rating"] >= MIN_RATING:
            filtered.append(row)
    return filtered


def sort_by_deal_score(rows):
    # Simple insertion sort to keep full manual control over the comparison logic
    # (swap for rows.sort(...) at scale; kept explicit here to show the logic).
    for i in range(1, len(rows)):
        key_row = rows[i]
        j = i - 1
        while j >= 0 and rows[j]["deal_score"] < key_row["deal_score"]:
            rows[j + 1] = rows[j]
            j -= 1
        rows[j + 1] = key_row
    return rows


def main():
    raw_rows = load_raw_rows(INPUT_FILE)
    print(f"Loaded {len(raw_rows)} raw rows from {INPUT_FILE}")

    cleaned = []
    dropped_incomplete = 0
    for row in raw_rows:
        cleaned_row = clean_row(row)
        if cleaned_row is None:
            dropped_incomplete += 1
        else:
            cleaned.append(cleaned_row)
    print(f"Dropped {dropped_incomplete} rows with missing/corrupt price or rating")

    deduped, dup_count = deduplicate(cleaned)
    print(f"Removed {dup_count} duplicate SKUs")

    with_scores = add_derived_fields(deduped)
    filtered = filter_catalog(with_scores)
    print(f"Filtered to {len(filtered)} items (effective price <= Rs.{PRICE_CEILING}, rating >= {MIN_RATING})")

    ranked = sort_by_deal_score(filtered)

    fieldnames = ["sku_id", "brand", "category", "color", "season", "price_inr",
                  "discount_pct", "effective_price_inr", "rating", "num_ratings", "deal_score"]
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked)

    print(f"\nWrote {len(ranked)} ranked items to {OUTPUT_FILE}")
    print("\nTop 10 best deals:")
    print(f"{'SKU':<10}{'Brand':<12}{'Category':<14}{'Eff.Price':<12}{'Rating':<8}{'DealScore':<10}")
    for row in ranked[:10]:
        print(f"{row['sku_id']:<10}{row['brand']:<12}{row['category']:<14}"
              f"{row['effective_price_inr']:<12}{row['rating']:<8}{row['deal_score']:<10}")

    # Category-wise summary (built with plain dicts, no pandas)
    category_totals = {}
    for row in ranked:
        cat = row["category"]
        if cat not in category_totals:
            category_totals[cat] = {"count": 0, "price_sum": 0.0, "rating_sum": 0.0}
        category_totals[cat]["count"] += 1
        category_totals[cat]["price_sum"] += row["effective_price_inr"]
        category_totals[cat]["rating_sum"] += row["rating"]

    print("\nCategory summary (avg effective price / avg rating):")
    for cat, stats in sorted(category_totals.items(), key=lambda x: -x[1]["count"]):
        avg_price = stats["price_sum"] / stats["count"]
        avg_rating = stats["rating_sum"] / stats["count"]
        print(f"  {cat:<14} count={stats['count']:<5} avg_price=Rs.{avg_price:.2f}  avg_rating={avg_rating:.2f}")


if __name__ == "__main__":
    main()
