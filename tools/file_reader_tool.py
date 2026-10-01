from tools.file_reader import file_reader
from tools.tool import Tool


file_reader_tool = Tool(
    name="file_reader",
    description="Reads the contents of a local text file.",
    function=file_reader,
    parameters={
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": (
                    "Path of the local text file to read."
                )
            }
        },
        "required": ["file_path"]
    }
)