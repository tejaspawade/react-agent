from tools.search import search
from tools.tool import Tool

search_tool = Tool(
    name="search",
    description="Searches Wikipedia for factual information.",
    function=search,
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The topic or question to search for."
            }
        },
        "required": ["query"]
    }
)