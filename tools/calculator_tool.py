from tools.calculator import calculator
from tools.tool import Tool


calculator_tool = Tool(
    name="calculator",
    description="Performs mathematical calculations.",
    function=calculator,
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "Mathematical expression to calculate."
            }
        },
        "required": ["expression"]
    }
)