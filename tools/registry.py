from tools.tool import Tool


class ToolRegistry:

    def __init__(self):
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self.tools.values())

    def get_schemas(self) -> list[dict]:
        return [
            tool.to_schema()
            for tool in self.tools.values()
        ]

    def get_gemini_declarations(self) -> list[dict]:
        return [
            tool.to_gemini_declaration()
            for tool in self.tools.values()
        ]