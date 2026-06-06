EXAMPLES = """
Example 1: Category Efficiency Matrix (Revenue and Profit Margin % by Sub_Category)
Question: Which product sub-categories are our highest volume drivers and what are their profit margins?
SQL:
SELECT
    p."Sub-Category",
    SUM(f."Sales") AS "Total Revenue",
    (SUM(f."Profit") / SUM(f."Sales")) * 100 AS "Profit Margin %"
    FROM fact_sales f
    JOIN dim_product p ON f."ProductRowID" = p."ProductRowID"
    GROUP BY p."Sub-Category"
    ORDER BY "Total Revenue" DESC;

Example 2: Region PERFORMANCE (Revenue and Profit by Region)
Question: Show total revenue and profit across our different regions.
SQL:
SELECT
    r."Region",
    SUM(f."Sales") AS "Total Revenue",
    SUM(f."Profit") AS "Total Profit"
FROM fact_sales f
JOIN dim_region r ON f."RegionKey" = r."RegionKey"
GROUP BY r."Region"
ORDER BY "Total Revenue" DESC;

Example 3: 7-Day Rolling Revenue Trend
Question: Give me the monthly trend of our daily revenue along its 7-day rolling average baseline.
SQL:
WITH DailySales AS (
    SELECT
        d."Order Date",
        SUM(f."Sales") AS DailyRevenue
    FROM fact_sales f
    JOIN dim_date d ON f."Order Date" = d."Order Date"
    GROUP BY d."Order Date"
    )
SELECT
    "Order Date",
    DailyRevenue,
    AVG(DailyRevenue) OVER (ORDER BY "Order Date" ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS "7-Day Rolling Revenue"
FROM DailySales
Order BY "Order Date" DESC;

Example 4: Operational Leakage Tracker (Outlier Hits)
Question: Identify our top 5 worst un-profitable orders causing operational leakage.
SQL:
SELECT
    f."Order ID",
    p."Product Name",
    SUM(f."Sales") AS "Total Revenue",
    SUM(f."Profit") AS "Total Profit",
    f."Discount"
FROM fact_sales f
JOIN dim_product p ON f."ProductRowID" = P."ProductRowID"
GROUP BY f."Order ID", p."Product Name", f."Discount"
HAVING SUM(f."Profit") < 0
ORDER BY "Total Profit" ASC
LIMIT 5;
"""