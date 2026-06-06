import streamlit as st
import sqlite3
import pandas as pd
import google.generativeai as genai
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from rag.prompt_builder import build_prompt

if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else: 
    st.error("Missing Gemini API Key! Please create your `.streamlit/secrets.toml` file.")
    st.stop()
genai.configure(api_key=API_KEY)
system_rules = """
    You are a precise SQLite SQL generating engine.
    Return ONLY a valid, executable SQLite raw SQL query string.
    Do NOT include markdown block formatting, markdown code fences, backticks, or text explanantions.
    CRITICAL RULE FOR COLUMNS WITH SPACES:
    Every time you reference a column name that contains a space, you MUST wrap it in double quotes, even when using table aliases!
    Examples: 
    - Use f."Region Key" instead of f.Region Key
    - Use f."ProductRowID" instead of f.ProductRowID
    - Use d."Order Date" instead of d.Order Date
    """
model = genai.GenerativeModel(model_name = "gemini-2.5-flash", system_instruction=system_rules)
conn = sqlite3.connect("database/sales.db", check_same_thread=False)
st.set_page_config(page_title="AI Sales Analytics Copilot", layout="wide")
st.title("📊AI Sales Analytics Copilot")
st.caption("Synchronized with your Star-Schema Power BI Dashboard Metrics")
question = st.text_input("💬 Ask a business question about revenue, margins, rolling trends, or operational leaks:")
def clean_sql(sql):
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()
def run_sql(sql):
    cleaned = clean_sql(sql)
    return pd.read_sql(cleaned, conn)
def generate_sql(question):
    raw_prompt = build_prompt(question)
    response = model.generate_content(raw_prompt)
    return response.text
def explain(question, df):
    prompt = f"""
    You are a Lead Business Data Analyst looking at executive metrics.
    
    Context: A business user asked: "{question}"
    The SQL query exectued on our Star Schema database returned this performance data:
    {df.head(15).to_string(index=False)}
    
    Provide a professional, concise executive assessment including:
    1. **Key Operational Insight** (Connect volumes to profit margins)
    2. **Trend Vector** (Explain whether this performance represents an isolated event or systematic pattern)
    3. **Strategic Recommendation** (What concrete operational decision should management execute right now?)
    """
    response = model.generate_content(prompt)
    return response.text
if st.button("Run Analytics Engine"):
    if question.strip() == "":
        st.warning("Please enter a business question first.")
    else:
        with st.spinner("Analyzing database schemas and tracking dashboard metrics..."):
            try:
                sql_query = generate_sql(question)
                col1, col2 = st.columns([1,1])
                with col1:
                    st.subheader("🛠️ Compiled SQL Query")
                    st.code(clean_sql(sql_query), language="sql")
                df_result = run_sql(sql_query)
                with col2:
                    st.subheader("📈 Retrieved Dataset")
                    st.dataframe(df_result, use_container_width=True)
                st.markdown("---")
                st.subheader("💡 Executive Synthesis & Recommendations")
                insights_brief = explain(question, df_result)
                st.write(insights_brief)
            except Exception as e:
                st.error(f"Operation Execution Error: {e}")