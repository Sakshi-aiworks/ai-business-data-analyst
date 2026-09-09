from ollama import chat

from src.analysis import (
    total_sales,
    total_profit,
    top_product,
    sales_by_region,
    sales_by_product,
    sales_over_time,
    calculate_sum,
    calculate_average,
    calculate_min,
    calculate_max,
    group_by_column,
    top_value,
)


# ==================================================
# DATASET SCOPE CHECK
# ==================================================


def check_question_scope(question):
    """
    Prevent obvious non-business-data questions.

    The agent should answer questions using the
    uploaded dataset, not general internet knowledge.
    """

    question = question.lower()

    unsupported_topics = [
        "weather",
        "capital of",
        "president of",
        "prime minister of",
        "stock price",
        "news",
        "movie",
        "football",
        "cricket score",
    ]

    for topic in unsupported_topics:
        if topic in question:
            return False

    return True


# ==================================================
# CREATE TOOLS
# ==================================================


def create_tools(df):

    # --------------------------------------------------
    # Existing sales tools
    # --------------------------------------------------

    def get_total_sales():
        """Get total sales from the dataset."""
        return total_sales(df)

    def get_total_profit():
        """Get total profit from the dataset."""
        return total_profit(df)

    def get_top_product():
        """Get the product with the highest total sales."""
        return top_product(df)

    def get_sales_by_region():
        """Get total sales grouped by region."""
        return sales_by_region(df).to_dict()

    def get_sales_by_product():
        """Get total sales grouped by product."""
        return sales_by_product(df).to_dict()

    def get_sales_over_time():
        """Get sales grouped by date."""
        return sales_over_time(df).to_dict()

    # --------------------------------------------------
    # Generic tools
    # --------------------------------------------------

    def generic_sum(column):
        """
        Calculate the total of any numeric column.
        """
        return calculate_sum(df, column)

    def generic_average(column):
        """
        Calculate the average of any numeric column.
        """
        return calculate_average(df, column)

    def generic_min(column):
        """
        Find the minimum value of any numeric column.
        """
        return calculate_min(df, column)

    def generic_max(column):
        """
        Find the maximum value of any numeric column.
        """
        return calculate_max(df, column)

    def generic_group_by(
        group_column,
        value_column
    ):
        """
        Group one column and calculate the sum
        of another numeric column.
        """
        return group_by_column(
            df,
            group_column,
            value_column
        ).to_dict()

    def generic_top_value(
        group_column,
        value_column
    ):
        """
        Find the category with the highest
        total value.

        Example:
        Customer + Revenue
        -> customer with highest revenue
        """
        result = top_value(
            df,
            group_column,
            value_column
        )

        return result

    # ==================================================
    # TOOL DEFINITIONS
    # ==================================================

    tools = [

        # --------------------------------------------------
        # Sales tools
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "get_total_sales",
                "description": (
                    "Use only when the dataset contains a "
                    "'Sales' column and the user asks for "
                    "total, overall, or combined sales."
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
                    "Use only when the dataset contains a "
                    "'Profit' column and the user asks for "
                    "total, overall, or combined profit."
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
                    "Use only for datasets containing Product "
                    "and Sales columns. Finds the product with "
                    "the highest total sales."
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
                    "Use only for datasets containing Region "
                    "and Sales columns. Returns sales grouped "
                    "by region."
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
                    "Use only for datasets containing Product "
                    "and Sales columns. Returns sales grouped "
                    "by product."
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
                "name": "get_sales_over_time",
                "description": (
                    "Use only for datasets containing Date "
                    "and Sales columns. Returns sales over time."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
        },

        # --------------------------------------------------
        # Generic SUM
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_sum",
                "description": (
                    "Calculate the total/sum of a numeric "
                    "column from the uploaded dataset. "
                    "Use this for questions such as total "
                    "Revenue, total Orders, total Salary, etc."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric "
                                "column to sum."
                            ),
                        }
                    },
                    "required": ["column"],
                },
            },
        },

        # --------------------------------------------------
        # Generic AVERAGE
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_average",
                "description": (
                    "Calculate the average/mean of a numeric "
                    "column from the uploaded dataset."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric "
                                "column to average."
                            ),
                        }
                    },
                    "required": ["column"],
                },
            },
        },

        # --------------------------------------------------
        # Generic MIN
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_min",
                "description": (
                    "Find the minimum/smallest value of a "
                    "numeric column."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric column."
                            ),
                        }
                    },
                    "required": ["column"],
                },
            },
        },

        # --------------------------------------------------
        # Generic MAX
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_max",
                "description": (
                    "Find the maximum/largest value of a "
                    "numeric column."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric column."
                            ),
                        }
                    },
                    "required": ["column"],
                },
            },
        },

        # --------------------------------------------------
        # Generic GROUP BY
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_group_by",
                "description": (
                    "Group the dataset by a text/category "
                    "column and calculate the sum of a numeric "
                    "column. Use for questions such as "
                    "'revenue by customer', 'sales by country', "
                    "or 'orders by department'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_column": {
                            "type": "string",
                            "description": (
                                "Exact name of the category/text "
                                "column used for grouping."
                            ),
                        },
                        "value_column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric column "
                                "to aggregate."
                            ),
                        },
                    },
                    "required": [
                        "group_column",
                        "value_column",
                    ],
                },
            },
        },

        # --------------------------------------------------
        # Generic TOP VALUE
        # --------------------------------------------------

        {
            "type": "function",
            "function": {
                "name": "generic_top_value",
                "description": (
                    "Find the category/text value with the "
                    "highest total of a numeric column. "
                    "Use for questions such as 'best customer', "
                    "'customer with highest revenue', "
                    "'top department by salary', or "
                    "'country with highest sales'."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_column": {
                            "type": "string",
                            "description": (
                                "Exact name of the category/text "
                                "column."
                            ),
                        },
                        "value_column": {
                            "type": "string",
                            "description": (
                                "Exact name of the numeric "
                                "column to compare."
                            ),
                        },
                    },
                    "required": [
                        "group_column",
                        "value_column",
                    ],
                },
            },
        },
    ]

    # ==================================================
    # FUNCTION MAP
    # ==================================================

    available_functions = {

        "get_total_sales":
            get_total_sales,

        "get_total_profit":
            get_total_profit,

        "get_top_product":
            get_top_product,

        "get_sales_by_region":
            get_sales_by_region,

        "get_sales_by_product":
            get_sales_by_product,

        "get_sales_over_time":
            get_sales_over_time,

        "generic_sum":
            generic_sum,

        "generic_average":
            generic_average,

        "generic_min":
            generic_min,

        "generic_max":
            generic_max,

        "generic_group_by":
            generic_group_by,

        "generic_top_value":
            generic_top_value,
    }

    return tools, available_functions


# ==================================================
# RUN AGENT
# ==================================================


def run_agent(df, question):

    # --------------------------------------------------
    # 1. Basic scope check
    # --------------------------------------------------

    if not check_question_scope(question):

        return (
            "I can't answer that because it is outside "
            "the scope of the uploaded business dataset."
        )

    # --------------------------------------------------
    # 2. Create tools
    # --------------------------------------------------

    tools, available_functions = create_tools(df)

    # --------------------------------------------------
    # 3. Give the LLM the dataset schema
    # --------------------------------------------------

    columns = df.columns.tolist()

    numeric_cols = df.select_dtypes(
        include="number"
    ).columns.tolist()

    text_cols = df.select_dtypes(
        include=[
            "object",
            "string",
            "category"
        ]
    ).columns.tolist()

    schema_context = f"""
Dataset information:

Columns:
{columns}

Numeric columns:
{numeric_cols}

Text/category columns:
{text_cols}

Rows:
{len(df)}
"""

    # --------------------------------------------------
    # 4. System instructions
    # --------------------------------------------------

    system_prompt = f"""
You are an AI Business Data Analyst.

You answer questions using ONLY the uploaded dataset
and the Python analysis tools provided to you.

{schema_context}

IMPORTANT RULES:

1. Never invent business information.

2. Never use your general knowledge to answer a
   business-data question.

3. If the requested information is not present in
   the dataset, clearly say that it is not available.

4. Before selecting a tool, carefully inspect the
   dataset columns provided above.

5. Use the exact column names from the dataset.

6. For numerical questions, ALWAYS use a Python
   analysis tool instead of doing calculations yourself.

7. "best", "top", "strongest", "highest", or
   "most successful" means the highest value when
   the question clearly refers to a numeric business
   metric.

8. For example:
   "best customer by revenue"
   means:
   group_column = Customer
   value_column = Revenue

9. For:
   "total revenue"
   use generic_sum with column = Revenue.

10. For:
   "average revenue"
   use generic_average with column = Revenue.

11. For:
   "revenue by customer"
   use generic_group_by with:
   group_column = Customer
   value_column = Revenue.

12. For:
   "customer with highest revenue"
   use generic_top_value with:
   group_column = Customer
   value_column = Revenue.

13. Do not answer questions about weather,
    geography, general knowledge, news, entertainment,
    or other information that is not contained in
    the uploaded dataset.

14. After receiving the Python result, explain it
    naturally and briefly.
"""

    # --------------------------------------------------
    # 5. Conversation
    # --------------------------------------------------

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
    # 6. Ask LLM to select a tool
    # --------------------------------------------------

    response = chat(
        model="qwen2.5:3b",
        messages=messages,
        tools=tools,
    )

    # --------------------------------------------------
    # 7. Tool call?
    # --------------------------------------------------

    if response.message.tool_calls:

        tool_call = response.message.tool_calls[0]

        function_name = tool_call.function.name

        function = available_functions.get(
            function_name
        )

        if function is None:

            return (
                "I couldn't determine the correct "
                "analysis for that question."
            )

        # --------------------------------------------------
        # 8. Get arguments
        # --------------------------------------------------

        arguments = tool_call.function.arguments

        # --------------------------------------------------
        # 9. Execute tool
        # --------------------------------------------------

        try:

            result = function(**arguments)

        except Exception as error:

            return (
                "I couldn't perform that analysis because "
                f"{str(error)}"
            )

        # --------------------------------------------------
        # 10. Add tool call + result
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
        # 11. Ask LLM to explain result
        # --------------------------------------------------

        final_response = chat(
            model="qwen2.5:3b",
            messages=messages,
        )

        return final_response.message.content

    # --------------------------------------------------
    # 12. No tool selected
    # --------------------------------------------------

    return response.message.content