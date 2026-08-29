from ollama import chat

from analysis import (
    total_sales,
    total_profit,
    top_product,
    sales_by_region,
    sales_by_product,
)


def check_question_scope(question):
    """
    Prevent the agent from answering questions about
    information that is not available in the current dataset.
    """

    question = question.lower()

    unsupported_topics = [
        "customer",
        "employee",
        "salary",
        "weather",
        "supplier",
        "vendor",
        "inventory",
        "order",
        "location",
    ]

    for topic in unsupported_topics:
        if topic in question:
            return False

    return True


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
    # 1. Safety / scope check
    # --------------------------------------------------

    if not check_question_scope(question):
        return (
            "I can't answer that from the available business data. "
            "The current dataset does not contain the information "
            "needed for this question."
        )

    # --------------------------------------------------
    # 2. Create tools
    # --------------------------------------------------

    tools, available_functions = create_tools(df)

    # --------------------------------------------------
    # 3. Conversation for the LLM
    # --------------------------------------------------

    messages = [
        {
            "role": "system",
            "content": """
You are an AI Business Data Analyst.

Your job is to answer questions using the available
business data and Python analysis tools.

IMPORTANT RULES:

1. Use a Python tool whenever the question requires
   information from the business dataset.

2. Never invent numbers, names, customers, employees,
   products, regions, or other business information.

3. "best product", "top product", "strongest product",
   "highest-selling product", and "most successful product"
   mean the product with the highest total sales.

4. Only use information returned by the Python tools
   when answering data-related questions.

5. If the available data does not contain the information
   needed to answer the question, clearly say that the
   information is not available.

6. After receiving a tool result, explain the result
   clearly and naturally.
""",
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
        # 7. Add tool request and actual result to messages
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