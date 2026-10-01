from google.genai import types

from agent.llm import GeminiLLM
from agent.prompts import REACT_SYSTEM_PROMPT
from agent.scratchpad import Scratchpad
from agent.memory import ConversationMemory

from tools.registry import ToolRegistry


class Agent:

    def __init__(
        self,
        llm: GeminiLLM,
        registry: ToolRegistry,
        max_iterations: int = 5
    ):
        self.llm = llm
        self.registry = registry
        self.max_iterations = max_iterations

        self.scratchpad = Scratchpad()
        self.memory = ConversationMemory()

    def execute_tool(
        self,
        tool_name: str,
        arguments: dict
    ):

        tool = self.registry.get(tool_name)

        if tool is None:
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}"
            }

        try:
            result = tool.function(
                **arguments
            )

            return {
                "status": "success",
                "result": result
            }

        except TypeError as e:
            return {
                "status": "error",
                "error": f"Invalid arguments: {str(e)}"
            }

        except Exception as e:
            return {
                "status": "error",
                "error": f"Tool execution error: {str(e)}"
            }

    def run(self, user_question: str) -> str:

        tools = self.registry.get_gemini_declarations()

        # -----------------------------------------
        # Reset scratchpad for the current task
        # -----------------------------------------

        self.scratchpad.clear()

        # -----------------------------------------
        # Add the new user question to memory
        # -----------------------------------------

        self.memory.add_user_message(
            user_question
        )

        # -----------------------------------------
        # Build Gemini conversation history
        # using only user + assistant messages
        # -----------------------------------------

        contents = []

        for message in self.memory.get_messages():

            contents.append(
                types.Content(
                    role=message["role"],
                    parts=[
                        types.Part.from_text(
                            text=message["content"]
                        )
                    ]
                )
            )

        # -----------------------------------------
        # Agent loop
        # -----------------------------------------

        for iteration in range(
            self.max_iterations
        ):

            print(
                f"\n--- Iteration {iteration + 1} ---"
            )

            response = self.llm.generate(
                contents=contents,
                tools=tools,
                system_instruction=REACT_SYSTEM_PROMPT
            )

            print("\nRaw Gemini response:")
            print(response)

            # -------------------------------------
            # Handle malformed function call
            # -------------------------------------

            finish_reason = (
                response.candidates[0].finish_reason
            )

            if (
                finish_reason.name
                == "MALFORMED_FUNCTION_CALL"
            ):
                return (
                    "The model returned a malformed "
                    "tool call. The agent stopped safely."
                )

            # -------------------------------------
            # Find ALL function calls
            # -------------------------------------

            function_calls = []

            for candidate in response.candidates:

                for part in candidate.content.parts:

                    if part.function_call:

                        function_calls.append(
                            part.function_call
                        )

            # -------------------------------------
            # No function call means final answer
            # -------------------------------------

            if not function_calls:

                final_answer = response.text

                # Store only the final answer
                # in conversation memory.

                self.memory.add_assistant_message(
                    final_answer
                )

                return final_answer

            # -------------------------------------
            # Store Gemini's tool-call response
            # ONLY in the current run.
            #
            # We do NOT add this to persistent
            # conversation memory.
            # -------------------------------------

            model_content = (
                response.candidates[0].content
            )

            contents.append(
                model_content
            )

            # -------------------------------------
            # Execute all requested tools
            # -------------------------------------

            for function_call in function_calls:

                tool_name = function_call.name

                arguments = dict(
                    function_call.args
                )

                print("\nTool requested:")
                print(tool_name)

                print("\nArguments:")
                print(arguments)

                # ---------------------------------
                # Prevent repeated tool calls
                # ---------------------------------

                if self.scratchpad.has_seen_action(
                    tool_name,
                    arguments
                ):

                    return (
                        "The agent detected a repeated "
                        "tool call and stopped to avoid "
                        "an infinite loop."
                    )

                # ---------------------------------
                # Execute tool
                # ---------------------------------

                tool_result = self.execute_tool(
                    tool_name,
                    arguments
                )

                print("\nTool result:")
                print(tool_result)

                # ---------------------------------
                # Store observation in scratchpad
                # ---------------------------------

                self.scratchpad.add_step(
                    tool_name=tool_name,
                    arguments=arguments,
                    observation=str(
                        tool_result
                    )
                )

                # ---------------------------------
                # Send tool result back to Gemini
                # ---------------------------------

                function_response_part = (
                    types.Part.from_function_response(
                        name=function_call.name,
                        response=tool_result
                    )
                )

                function_response_content = (
                    types.Content(
                        role="user",
                        parts=[
                            function_response_part
                        ]
                    )
                )

                # Tool response belongs to the
                # current agent run only.

                contents.append(
                    function_response_content
                )

            print("\nScratchpad:")
            print(
                self.scratchpad.render()
            )

        # -----------------------------------------
        # Maximum iteration limit reached
        # -----------------------------------------

        return (
            "The agent stopped because it "
            "reached the maximum limit of "
            f"{self.max_iterations} iterations."
        )