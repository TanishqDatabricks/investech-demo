"""Generates sales_orders.csv: a deliberately messy order export for the Genie Code CLI demos."""
import csv
import random
from datetime import date, timedelta

random.seed(42)
REGIONS = {"North America": ["North America", "north america", "NA ", "N. America"],
           "EMEA": ["EMEA", "emea", "Europe"],
           "APAC": ["APAC", "apac", "Asia Pacific"],
           "LATAM": ["LATAM", "Latin America"]}
PRODUCTS = [("SKU-1001", "Lakehouse Starter Kit", 1200.0), ("SKU-1002", "Streaming Add-on", 450.0),
            ("SKU-1003", "ML Training Credits", 800.0), ("SKU-1004", "Dashboard Seats (10)", 300.0),
            ("SKU-1005", "Premium Support", 2500.0), ("SKU-1006", "Data Sharing Pack", 650.0)]
CHANNELS = ["web", "partner", "direct", "marketplace"]
START = date(2026, 5, 1)

def fmt_date(d):
    # Mixed formats, as from several upstream systems.
    return random.choices([d.isoformat(), d.strftime("%m/%d/%Y"), d.strftime("%d-%b-%Y")], weights=[70, 20, 10])[0]

def fmt_amount(x):
    return random.choices([f"{x:.2f}", f"${x:,.2f}", f"{x:.0f}"], weights=[75, 20, 5])[0]

rows = []
for i in range(1, 1201):
    region = random.choices(list(REGIONS), weights=[45, 30, 18, 7])[0]
    sku, name, price = random.choice(PRODUCTS)
    qty = random.choices([1, 2, 3, 5, 10], weights=[50, 25, 12, 8, 5])[0]
    discount = random.choice([0, 0, 0, 0.05, 0.1, 0.15])
    d = START + timedelta(days=random.randint(0, 182))
    status = random.choices(["completed", "refunded", "cancelled", "pending"], weights=[82, 8, 6, 4])[0]
    amount = round(price * qty * (1 - discount), 2)
    row = {
        "order_id": f"ORD-{100000 + i}",
        "order_date": fmt_date(d),
        "customer_id": f"CUST-{random.randint(1, 340):04d}",
        "region": random.choice(REGIONS[region]),
        "channel": random.choice(CHANNELS),
        "product_sku": sku,
        "product_name": name,
        "quantity": str(qty),
        "unit_price": f"{price:.2f}",
        "discount_pct": f"{discount:.2f}",
        "order_amount": fmt_amount(amount),
        "status": status.upper() if random.random() < 0.1 else status,
        "refund_amount": fmt_amount(amount) if status == "refunded" else "",
        "refund_reason": random.choice(["damaged", "duplicate charge", "not as described", "changed mind"]) if status == "refunded" else "",
        "sales_rep": random.choice(["A. Patel", "J. Kim", "M. Garcia", "S. Okafor", "L. Chen", ""]),
    }
    # Data-quality problems a cleanup step should catch.
    r = random.random()
    if r < 0.02: row["customer_id"] = ""
    elif r < 0.035: row["region"] = ""
    elif r < 0.045: row["quantity"] = "-" + row["quantity"]
    elif r < 0.05: row["order_amount"] = "N/A"
    rows.append(row)

rows += [dict(random.choice(rows)) for _ in range(25)]  # duplicate records from a double export
random.shuffle(rows)
with open("sales_orders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(len(rows), "rows")
