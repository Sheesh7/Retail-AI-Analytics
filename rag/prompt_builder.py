from rag.schema import SCHEMA
from rag.examples import EXAMPLES

def build_prompt(question):
    return f"""
You are an expert data analyst generating SQL for SQLite.

{SCHEMA}

{EXAMPLES}

CRITICAL RULES:
1. ONLY output raw, executable SQL. No backticks, no markdown code blocks.
2. Every column or key with a space or capitalization MUST be fully double-quoted on BOTH sides of an equation or join condition.
   - WRONG: f."Region Key" = r.Region Key
   - CORRECT: f."RegionKey" = r."RegionKey"
3. Use fact_sales as the main table.

QUESTION:
{question}
"""