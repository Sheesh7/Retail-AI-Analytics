# 📊 AI Sales Analytics Copilot & BI Intelligence Engine

An enterprise-grade ecosystem that bridges an interactive **Retrieval-Augmented Generation (RAG) Text-to-SQL engine** with a formal relational **Star Schema**. The system incorporatesexploratory data profiling, unsupervised multivariate machine learning for anomaly detection, and advanced business intelligence to extract high-fidelity operational insights from retail transactional data.

---

## 🏗️ System Architecture & Data Engineering Pipeline

The architecture is built as synchronized pipeline that transforms flat, denormalized transactional ledgers into structured, context-aware intelligence.

```text
[Flat Transaction Data] ──> [EDA & Statistical Profiling] ──> [ETL & Dimensional Modeling]
│
┌────────────────────────────────────────────────────────────────┴────────────────────────────────┐
▼                                                                                                 ▼
[Targeted CSV Serialization]                                                                  [SQLite Relational DB]
│                                                                                                 │
▼                                                                                                 ▼
[Power BI Dashboard Layer]                                                                    [LLM RAG Context Injection]
│
▼
[Streamlit Analytics Copilot]
```

1. **Exploratory Data Analysis (EDA) & Profiling:** Ingestion of baseline data (`samplesuperstore.csv`), mapping of dynamic data types, validation of temporal vector, and statistical shape analysis.
2. **ETL & Dimnesional Modeling:** Decomposition of denormalized records into a structured SQLite relational database engine (`sales.db`) utilizing of surrogate keys and optimal database join paths.
3. **Downstream CSV Serialization:** Extraction of isolated dimension and fact datasets into targeted CSV layers to serve as high-performance data sources for the Power BI Dashboard.
4. **Natural Language Interface (RAG/Copilot):** An interactive Streamlit web interface leveraging **Gemini 2.5 Flash** to compile natural language business questions into raw, runtime-executable SQLite queries based on the database metadata context.

---

## 🧠 Deep-Dive Data Science, Machine Learning & Statistical Methodologies

This project moves beyond standard descriptibe reporting by embedding mathematical and statistical frameworks directly into analytical processing layer to isolate riskand quantify performance.

### 1. Statistical Data Distribution & Shape Profiling
Before modeling, the underlying distribution of independent transactional features (`Sales`, `Profit`) is mapped using higher-order statistical moments via Pandas aggregation (`.agg(["mean", "median", "std", "skew", "kurtosis"])`):
* **Skewness ($G_1$):** Measures the asymmetry of the sales distribution around its mean. A highly positive skewness indicates a heavy right-tailed distribution, revealing an operation dominated by high-frequency, low-to-mid value transactions interspersed with intermittent high-value purchase spikes.
* **Kurtosis ($G_2$):** Measures the "tailedness" of the probability distribution. The extreme positive kurtosis confirms a **leptokurtic distribution**. This mathematically proves that operational tail-risk events (e.g., massive single-order revenue volumes or deep-discount loss leaks) occur far more frequently than a standard Gaussian distribution would predict.

### 2. Feature Interdependence & Multicollinearity
Through Pearson Correlation coefficients ($r$), a linear covariance matrix evaluates dependencies across continuous features: `Sales`, `Profit`, `Quantity`, and `Discount`.
$$\rho_{X,Y} = \frac{\operatorname{cov}(X,Y)}{\sigma_X \sigma_Y}$$
This structure evaluates **multicollinearity**—specifically verifying whether aggressive promotional discount rates exhibit an unsustainable negative covariance with net profit margins, allowing analysts to distinguish between healthy volume scaling and margin-degrading growth.

### 3. Pareto Principle (80/20 Rule) for Revenue Concentration
The codebase executes programmatic **Pareto Concentration Analysis** by ordering transactions by descending monetary value and evaluating the cumulative density function:
```python
top_20_pct = df.sort_values("Sales", ascending=False).head(int(len(df) * .2))
concentration = top_20_pct["Sales"].sum() / df["Sales"].sum()
```

### 4. Advanced Operational Leakage & Outlier Detection Frameworks

To identify operational leakage, the system deploys a multi-layered anomaly detection architecture spanning non-parametric statistical metrics, specialized domain logic, and unsupervised machine learning:

#### Univariate Outlier Isolation via Interquartile Range (IQR)
To handle highly skewed retail data without assuming normal distribution, the system calculates boundaries using the 25th ($Q_1$) and 75th ($Q_3$) percentiles:

$$\text{IQR} = Q_3 - Q_1$$
$$\text{Upper Boundary} = Q_3 + 1.5 \times \text{IQR}$$

Any transaction crossing this upper limit is isolated as an independent, statistically anomalous sales volume event.

#### Domain-Specific 'Business Outliers'
The engine isolates transactions operating at the intersection of high sales volume and net negative financial returns:

$$\text{Business Outliers} = \{x \mid x_{\text{Sales}} \ge \text{90th Percentile} \ \wedge \ x_{\text{Profit}} < 0\}$$

This exposes structural pricing or logistical execution breakdowns where the company loses capital on its largest delivery contracts.

#### Multivariate Unsupervised Machine Learning via Isolation Forest
Because revenue leaks often involve subtle interactions across multiple features, an Isolation Forest ensemble algorithm is trained on a multi-dimensional feature space ($X = [\text{Sales}, \text{Profit}, \text{Discount}]$):

```python
from sklearn.ensemble import IsolationForest
iso_forest = IsolationForest(contamination=0.01, random_state=42)
df['is_anomaly'] = iso_forest.fit_predict(df[['Sales', 'Profit', 'Discount']])
```

Instead of modeling normal data patterns, the Isolation Forest isolates anomalies by randomly partitioning feature paths. Outliers travel significantly shorter path lengths through the decision tree structures because their attribute combinations are sparse and irregular. This flags multi-dimensional anomalies—such as a mid-tier sales volume combined with a high discount rate—that would completely bypass basic univariate filters.

---

### 5. Chronological Window Functions & Moving Averages

To smooth out weekly operational noise and uncover macro-level trends, the SQL layer uses analytical window functions to calculate a 7-Day Rolling Moving Average:

$$\text{SMA}_t = \frac{1}{N}\sum_{i=0}^{N-1} \text{Revenue}_{t-i}$$

```sql
AVG(DailyRevenue) OVER (
    ORDER BY "Order Date" 
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
) AS "7-Day Rolling Revenue"
```

This acts as a low-pass filter on high-frequency transaction data, separating day-of-week anomalies from true business growth vectors.

---

### 🗄️ Database Dimensional Modeling (Star Schema)

To provide reliable metrics across both the LLM RAG application and the Power BI dashboard, the denormalized transactional history is decomposed into an optimized Star Schema. This enforces strict relational integrity and minimizes analytical join costs.

```text
       ┌────────────────────────┐             ┌────────────────────────┐
       │      dim_product       │             │       dim_region       │
       ├────────────────────────┤             ├────────────────────────┤
       │ PK  ProductRowID       │             │ PK  RegionKey          │
       │     Product ID         │             │     Region             │
       │     Product Name       │             └───────────┬────────────┘
       │     Category           │                         │
       │     Sub-Category       │                         │ 1
       └───────────┬────────────┘                         │
                   │ 1                                    │
                   │                                      │
                   │               fact_sales             │
                   │       ┌──────────────────────┐       │
                   └─────> │ FK  ProductRowID     │ <─────┘
                           │ FK  RegionKey        │
                           │ FK  Order Date       │ ───┐
                           │     Row ID           │    │
                           │     Order ID         │    │
                           │     Sales            │    │
                           │     Profit           │    │ 1
                           │     Quantity         │    │
                           │     Discount         │    │
                           └──────────────────────┘    │
                                                       ▼
                                           ┌────────────────────────┐
                                           │        dim_date        │
                                           ├────────────────────────┤
                                           │ PK  Order Date         │
                                           │     Order Year         │
                                           │     Order Month        │
                                           │     Order ID           │
                                           └────────────────────────┘
```

#### Fact Table
* **fact_sales**: Stores transactional metrics (Sales, Profit, Quantity, Discount) paired with optimized foreign integer keys mapped directly to surrounding dimensions.

#### Dimension Tables
* **dim_product**: Handles product properties (Product ID, Product Name, Category, Sub-Category) anchored by an auto-incremented surrogate key (ProductRowID).
* **dim_region**: Consolidates regional structures to enable clean geographic performance breakdowns.
* **dim_date**: Isolates chronological markers (Order Date, Order Year, Order Month) to prevent runtime date parsing bottlenecks during complex window queries.

---

### 🤖 LLM Engine & RAG Metastore Construction

The text-to-SQL interface uses strict Prompt Engineering / Few-Shot In-Context Learning to turn natural language into reliable SQLite queries without the overhead of fine-tuning models.

* **Deterministic Rule Injection**: System-level routing flags force the LLM to output only raw, executable text strings. This strips out markdown code fences (such as \`\`\`sql), preventing syntax errors in the database driver.
* **Syntactic Guardrails**: Explicit string-handling instructions force double quotes around columns containing whitespace or camelCase attributes (e.g., `f."Order Date"`, `f."ProductRowID"`). This ensures perfect alignment with the Star Schema definition.
* **Two-Stage Executive Synthesis**:
    1. **Query Generation & Execution**: Translates user questions into optimized SQL commands, targets the local relational database, and returns tabular data via Pandas (`pd.read_sql`).
    2. **Strategic Analytical Formulation**: Feeds the resulting dataset into a secondary generative prompt. Here, the LLM acts as a Lead Business Data Analyst to provide executive insights, trend vectors, and concrete strategic recommendations.

---

### 💻 Technical Stack & Environment Layout

* **Language Platform**: Python 3.10+
* **Interface Engine**: Streamlit (UI rendering, asynchronous session states, and configuration secrets injection)
* **Inference Core**: Google Generative AI (gemini-2.5-flash)
* **Storage Engine**: SQLite3 Relational Database Engine
* **Vector Manipulation & Machine Learning**: Pandas, Scikit-Learn, NumPy
* **Visualization Layer**: Power BI Desktop (Retail Analytics Dashboard.pbix), Matplotlib

#### Project File Structure
```text
├── data/
│   ├── samplesuperstore.csv         # Raw transactional ledger
│   ├── fact_sales.csv               # Exported clean Fact table
│   ├── dim_product.csv              # Exported Product Dimension
│   ├── dim_region.csv               # Exported Region Dimension
│   └── dim_date.csv                 # Exported Date Dimension
├── database/
│   └── sales.db                     # Active compiled SQLite Database
├── notebook/
│   └── week1_analysis.ipynb       # Jupyter notebook for ETL & Machine Learning
├── rag/
│   ├── examples.py                  # Few-shot SQL execution context pairs
│   ├── schema.py                    # Schema metadata definitions
│   └── prompt_builder.py            # Context assembly module
├── app/
│   └── rag_app.py                   # Streamlit Copilot web interface
├── bi/
│   └── Retail Analytics Dashboard.pbix # Desktop Power BI analytical file
    └── requirements.txt
└── README.md                        # Documentation
```

---

### 🚀 Setup & Execution Guide

#### 1. Environment Initialization
Clone the repository and install the required dependencies within a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
#### 2. Configure Streamlit Security Keys
Create a local secrets file at `.streamlit/secrets.toml` to securely store your API credentials:

```toml
GEMINI_API_KEY = "YOUR_PRODUCTION_GEMINI_API_KEY_HERE"
```

#### 3. Run the ETL Pipeline & Build the Database
Run your notebook or execute your script to process the raw records, generate the SQLite schema tables, and export the clean CSV files for Power BI:

```bash
# Script processes data, executes SQL transformations, and writes out data assets
python notebook/build_star_schema.py
```

#### 4. Launch the AI Analytics Copilot
Start the Streamlit analytical user interface:

```bash
streamlit run app/rag_app.py
```

#### 5. Synchronize the Power BI Dashboard
Open `bi/Retail Analytics Dashboard.pbix` in Power BI Desktop. The report handles the relational schema automatically using the serialized CSV datasets located in your `data/` directory. This keeps your dashboard visuals perfectly in sync with semantic metrics calculated by your AI Copilot.