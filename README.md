# Fashion Tech Analyst Portfolio — Sarwagya Joshi

Three self-built projects backing the resume. All code actually runs — you can open,
run, and modify every file. Read this before interviews so you can speak to each
project confidently and honestly.

## Important — be upfront about data sources if asked
All three projects use **synthetic datasets I generated myself** (not scraped from a
live e-commerce site), because building/testing the logic doesn't require real data —
it requires *realistic* data. If an interviewer asks "is this real Myntra/Ajio data?",
the honest and completely fine answer is:
> "I generated a structurally realistic synthetic dataset to build and test the
> pipeline. The cleaning/analysis logic works identically on real scraped or API data —
> swapping the data source is a one-line change."
This is a normal, respected practice in data projects. Don't claim it's real scraped data.

---

## Project 1: Fashion Catalog Cleaning & Ranking Engine (Python)
**Folder:** `python_catalog_cleaner/`
**Files:** `generate_dataset.py`, `fashion_catalog_raw.csv` (1,230 rows), `clean_catalog.py`, `cleaned_catalog.csv`

What it does:
- Loads a messy 1,230-row fashion catalog (missing prices/ratings, duplicate SKUs,
  inconsistent casing/whitespace — realistic scraped-data problems)
- Cleans and normalizes text fields, drops incomplete rows, removes duplicate SKUs
- Computes an effective (discounted) price and a custom "deal score" per item
- Filters to sub-Rs.5000, rating >= 3.5 items, then ranks with a hand-written
  insertion sort (deliberately manual, not `.sort()`, to demonstrate the logic)
- Outputs a category-wise summary using plain dictionaries (no pandas)

Run it yourself:
```
cd python_catalog_cleaner
python3 generate_dataset.py   # regenerates the raw dataset (optional, already included)
python3 clean_catalog.py      # runs the cleaning pipeline, prints summary, writes cleaned_catalog.csv
```

Interview talking point: "I process each row through explicit validation and
normalization steps rather than relying on a library's default behavior, so I can
explain and defend exactly why any given item was kept, dropped, or ranked where it is."

---

## Project 2: Seasonal Fashion Trend Tracker (Excel)
**Folder:** `excel_trend_tracker/`
**Files:** `generate_inventory_data.py`, `raw_inventory.csv`, `build_workbook.py`, `Fashion_Trend_Tracker.xlsx`

What it does — 3 sheets, all formula-driven (not hardcoded numbers):
- **Raw_Inventory**: 72 rows of monthly sell-through data across 6 categories x 4 seasons
- **Seasonal_Summary**: a pivot-style table (Category x Season) built with
  `SUMIFS`/`AVERAGEIFS` — total units sold, avg stock, avg price, avg discount, and a
  computed "stock cover ratio" that flags fast-fashion demand spikes needing restock
- **SKU_Lookup**: type any SKU into the yellow input cell and every attribute
  auto-populates via `INDEX`/`MATCH`

Note on XLOOKUP: I used `INDEX`/`MATCH` instead of `XLOOKUP` in this file only because
the sandbox's recalculation engine (LibreOffice) can't evaluate `XLOOKUP` reliably —
`INDEX`/`MATCH` is functionally identical and is what `XLOOKUP` compiles down to
conceptually. In real Excel (which you'll use at the internship), you can write this
exact lookup as a single `XLOOKUP` formula — worth doing once you're on a real Excel
install, and mentioning both versions shows you understand *why* XLOOKUP exists, not
just that you can type it.

Interview talking point: "The summary sheet recalculates automatically if the raw
data changes — nothing is a pasted-in number — which is how I'd want an inventory
dashboard to behave in production."

---

## Project 3: Algorithmic Logic Optimization — Inventory Routing (C)
**Folder:** `c_inventory_routing/`
**Files:** `inventory_routing.c`, `inventory_routing` (compiled binary)

What it does:
- Models a warehouse picking problem: 10 SKUs across 5 zones with distances to the
  packing station
- **Merge sort** (O(n log n), written from scratch — no `qsort`) orders items by zone
  so a picker's route is efficient, then totals the route distance
- **Binary search** (O(log n)) looks up a SKU's zone once the array is sorted by SKU

Run it yourself:
```
cd c_inventory_routing
gcc -O2 -Wall -o inventory_routing inventory_routing.c
./inventory_routing
```

Interview talking point: "This is a small model of a real fulfilment-center problem —
picking-route optimization and fast SKU lookup are exactly what a WMS (warehouse
management system) does at scale. I wanted to show the underlying algorithmic
reasoning, not just call a library sort."

---

## How these map to your resume bullets
See the updated resume — each bullet below is now defensible because the file behind
it actually exists and runs:
- "Engineered a Python pipeline that cleaned, deduplicated, and ranked 1,230 fashion
  SKUs by a custom deal-score metric, cutting incomplete/duplicate listings by ~11%."
- "Modelled a formula-driven Excel seasonal demand tracker (SUMIFS/AVERAGEIFS,
  INDEX/MATCH) across 6 categories and 4 seasons to flag fast-fashion restock needs."
- "Implemented merge sort and binary search in C to optimize a mock warehouse picking
  route and SKU lookup, reducing lookup complexity from O(n) to O(log n)."
