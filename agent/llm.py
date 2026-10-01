import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class GeminiLLM:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

    def generate(
    self,
    contents,
    tools: list[dict] | None = None,
    system_instruction: str | None = None
    ):

        config = None

        if tools or system_instruction:

            config = types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        function_declarations=tools
                    )
                ] if tools else None,

                system_instruction=system_instruction
            )

        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=contents,
            config=config
        )

        return response