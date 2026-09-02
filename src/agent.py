from ollama import chat

from src.analysis import (
    total_sales,
    total_profit,
    top_product,
    sales_by_region,
    sales_by_product,
)


def create_tools(df):

    def get_total_sales():
        """Get the total sales from the business data."""
        return total_sales(df)

    def get_total_profit():
        """Get the total profit from the business data."""
        return total_profit(df)

    def get_top_product():
        """
        Get the product with the highest total sales.
        Best/top/strongest product means highest sales.
        """
        return top_product(df)

    def get_sales_by_region():
        """Get total sales grouped by region."""
        return sales_by_region(df).to_dict()

    def get_sales_by_product():
        """Get total sales grouped by product."""
        return sales_by_product(df).to_dict()

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_total_sales",
                "description": (
                    "Use this when the user asks about total, overall, "
                    "or combined sales."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_total_profit",
                "description": (
                    "Use this when the user asks about total, overall, "
                    "or combined profit."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_top_product",
                "description": (
                    "Use this when the user asks for the best, top, "
                    "strongest, highest-selling, or most successful "
                    "product based on sales."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_sales_by_region",
                "description": (
                    "Use this when the user asks about sales "
                    "by region or regional performance."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_sales_by_product",
                "description": (
                    "Use this when the user asks about sales "
                    "for different products or wants a product-wise "
                    "sales breakdown."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },
    ]

    available_functions = {
        "get_total_sales": get_total_sales,
        "get_total_profit": get_total_profit,
        "get_top_product": get_top_product,
        "get_sales_by_region": get_sales_by_region,
        "get_sales_by_product": get_sales_by_product,
    }

    return tools, available_functions


def run_agent(df, question):

    # --------------------------------------------------
    # 1. Read the actual dataset schema
    # --------------------------------------------------

    columns = list(df.columns)

    schema_text = ", ".join(columns)

    # --------------------------------------------------
    # 2. Create tools
    # --------------------------------------------------

    tools, available_functions = create_tools(df)

    # --------------------------------------------------
    # 3. Conversation for the LLM
    # --------------------------------------------------

    system_prompt = f"""
You are an AI Business Data Analyst.

You answer questions using the uploaded business
dataset and Python analysis tools.

CURRENT DATASET COLUMNS:

{schema_text}

IMPORTANT RULES:

1. Only answer questions using information that can
   be supported by the current dataset.

2. The available dataset columns are:
   {schema_text}

3. Never invent numbers, names, customers, employees,
   products, regions, or other business information.

4. If a question requires a column or information that
   does not exist in the dataset, clearly say that the
   information is not available.

5. Use a Python analysis tool whenever the question
   requires calculating information from the dataset.

6. Never guess the result of a calculation.

7. Only use information returned by the Python tools
   when answering data-related questions.

8. "best product", "top product", "strongest product",
   "highest-selling product", and "most successful product"
   mean the product with the highest total sales.

9. After receiving a tool result, explain the result
   clearly and naturally.

10. If the user's question is unrelated to the uploaded
    business data, explain that you can only answer
    questions supported by the uploaded dataset.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    # --------------------------------------------------
    # 4. Ask the LLM to select a tool
    # --------------------------------------------------

    response = chat(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools,
    )

    # --------------------------------------------------
    # 5. Check whether the LLM selected a tool
    # --------------------------------------------------

    if response.message.tool_calls:

        tool_call = response.message.tool_calls[0]

        function_name = tool_call.function.name

        function = available_functions.get(function_name)

        if function is None:
            return (
                "I couldn't determine the correct analysis "
                "for that question."
            )

        # --------------------------------------------------
        # 6. Execute the selected Python tool
        # --------------------------------------------------

        result = function()

        # --------------------------------------------------
        # 7. Add tool request and actual result
        # --------------------------------------------------

        messages.append(response.message)

        messages.append(
            {
                "role": "tool",
                "tool_name": function_name,
                "content": str(result),
            }
        )

        # --------------------------------------------------
        # 8. Ask LLM to explain the real result
        # --------------------------------------------------

        final_response = chat(
            model="qwen2.5:3b",
            messages=messages,
        )

        return final_response.message.content

    # --------------------------------------------------
    # 9. If no tool was selected
    # --------------------------------------------------

    return response.message.content