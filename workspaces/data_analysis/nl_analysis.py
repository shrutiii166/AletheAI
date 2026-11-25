import json
import re

import pandas as pd

from core.llm_connector import generate_response


def interpret_question(question, df):
    """Convert a natural-language question into a structured analysis plan."""

    columns = {
        column: str(df[column].dtype)
        for column in df.columns
    }

    prompt = f"""
You are a data analysis planner.

Convert the user's question into a JSON analysis plan.

Available columns and data types:
{json.dumps(columns, indent=2)}

Allowed operations:

1. summarize
   Use for general dataset summaries.

2. aggregate
   Fields: column, aggregation
   Aggregations: mean, sum, min, max, count, median

3. group_aggregate
   Fields: group_by, column, aggregation
   Aggregations: mean, sum, min, max, count, median

4. top_group
   Fields: group_by, column, aggregation, limit
   Use to find the best-performing or highest-value groups.

5. trend
   Fields: date_column, column, aggregation
   Use for changes over time.

6. outliers
   Fields: column
   Use to identify unusually high or low numeric values.

7. missing_values
   Use to inspect missing data.

Rules:
- Use only the available column names.
- Never invent column names.
- Choose the operation that best matches the question.
- Return ONLY valid JSON.
- Do not include markdown or explanations.

Example:
Question: Which category has the highest sales?

JSON:
{{
    "operation": "top_group",
    "group_by": "Category",
    "column": "Sales",
    "aggregation": "sum",
    "limit": 1
}}

User question:
{question}
"""

    response = generate_response(prompt=prompt)

    # Extract JSON even if the model adds surrounding text.
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("Couldn't interpret the question. Please rephrase it.")

    return json.loads(match.group())


def execute_analysis(df, plan):
    """Execute a validated analysis plan using Pandas."""

    operation = plan.get("operation")

    if operation == "summarize":
        return df.describe(include="all").transpose()

    if operation == "missing_values":
        result = df.isnull().sum()
        return result[result > 0].rename("Missing Values").to_frame()

    if operation == "aggregate":
        column = plan.get("column")
        aggregation = plan.get("aggregation")

        if column not in df.columns:
            raise ValueError("The requested column doesn't exist.")

        if aggregation not in ["mean", "sum", "min", "max", "count", "median"]:
            raise ValueError("Unsupported aggregation.")

        if aggregation != "count" and not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError("This calculation requires a numeric column.")

        return getattr(df[column], aggregation)()

    if operation in ["group_aggregate", "top_group"]:
        group_by = plan.get("group_by")
        column = plan.get("column")
        aggregation = plan.get("aggregation")

        if group_by not in df.columns or column not in df.columns:
            raise ValueError("One or more requested columns don't exist.")

        if aggregation not in ["mean", "sum", "min", "max", "count", "median"]:
            raise ValueError("Unsupported aggregation.")

        if aggregation != "count" and not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError("This calculation requires a numeric column.")

        result = (
            df.groupby(group_by)[column]
            .agg(aggregation)
            .reset_index()
            .sort_values(column, ascending=False)
        )

        if operation == "top_group":
            limit = plan.get("limit", 1)

            if not isinstance(limit, int) or not 1 <= limit <= 20:
                limit = 1

            result = result.head(limit)

        return result

    if operation == "trend":
        date_column = plan.get("date_column")
        column = plan.get("column")
        aggregation = plan.get("aggregation")

        if date_column not in df.columns or column not in df.columns:
            raise ValueError("One or more requested columns don't exist.")

        if aggregation not in ["mean", "sum", "min", "max", "count"]:
            raise ValueError("Unsupported aggregation.")

        if aggregation != "count" and not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError("The trend calculation requires a numeric column.")

        dates = pd.to_datetime(df[date_column], errors="coerce")

        valid = pd.DataFrame({
            "Date": dates,
            column: df[column],
        }).dropna(subset=["Date"])

        if valid.empty:
            raise ValueError("No valid dates were found in that column.")

        result = (
            valid.set_index("Date")[column]
            .resample("ME")
            .agg(aggregation)
            .reset_index()
        )

        return result

    if operation == "outliers":
        column = plan.get("column")

        if column not in df.columns:
            raise ValueError("The requested column doesn't exist.")

        if not pd.api.types.is_numeric_dtype(df[column]):
            raise ValueError("Outlier detection requires a numeric column.")

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        return df[
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        ]

    raise ValueError("I couldn't identify a supported analysis operation.")


def answer_data_question(question, df):
    """Interpret, calculate, and explain a natural-language data question."""

    plan = interpret_question(question, df)

    result = execute_analysis(df, plan)

    if isinstance(result, pd.DataFrame):
        result_text = result.to_string(index=False)
    else:
        result_text = str(result)

    explanation_prompt = f"""
You are AletheAI's data analysis assistant.

Explain the following calculated result to the user.

User's question:
{question}

Analysis performed:
{json.dumps(plan)}

Actual result calculated using Python and Pandas:
{result_text}

Instructions:
- Answer the user's question directly.
- Use only the supplied result.
- Do not invent numbers or conclusions.
- Explain important findings in simple language.
- If the result is empty, clearly say so.
- Keep the response concise.
"""

    explanation = generate_response(prompt=explanation_prompt)

    return {
        "answer": explanation,
        "result": result,
    }