SCHEMA = """
You are working with a sales analytics SQLite database configured in Star Schema.
Every business question MUST be answered using the explicit metric formulas defined below.

TABLE STRUCTURE:

fact_sales (
    "Row ID" INTEGER,
    "Order ID" TEXT,
    "Order Date" TEXT, -- Format: YYYY-MM-DD
    "ProductRowID" INTEGER, -- Foreign key to dim_product
    "RegionKey" INTEGER, -- Foreign key to dim_region
    "Sales" REAL, -- Raw revenue for the transaction
    "Profit" REAL, -- Raw profit/loss for the transaction
    "Quantity" Integer,
    "Discount" REAL
)

dim_product (
    "ProductRowID" TEXT PRIMARY KEY,
    "Product ID" TEXT,
    "Product Name" TEXT,
    "Category" TEXT,
    "Sub-Category" TEXT
)

dim_region (
    "RegionKey" INTEGER PRIMARY KEY,
    "Region" TEXT
)

dim_date (
    "Order Date TEXT PRIMARY KEY, -- FORMAT: YY-MM-DD
    "Order Year" INTEGER,
    "Order Month" TEXT,
    "Order Day" INTEGER
)

Relationships (JOIN PATHS):
- fact_sales."ProductRowID" = dim_product."ProductRowID"
- fact_sales."RegionKey" = dim_region."RegionKey"
- fact_sales. "Order Date" = dim_date."Order Date"

REQUIRED BUSINESS METRICS (DAX TO SQL ALIGNMENT):
- Total Revenue = SUM(fact_sales."Sales")
- Total Profit = SUM(fact_sales."Profit")
- Profit Margin % = (SUM(fact_sales."Profit") / SUM(fact_sales."Sales")) * 100
- 7-Day Rolling Revenue = An average of Total revenue over a 7-day window. In SQL:
AVG(DailyRevenue) OVER (ORDER BY "Order Date" ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
"""
