from agent.agent import Agent
from agent.llm import GeminiLLM

from tools.calculator_tool import calculator_tool
from tools.search_tool import search_tool
from tools.file_reader_tool import file_reader_tool

from tools.registry import ToolRegistry


def main():

    # -----------------------------------------
    # Create tool registry
    # -----------------------------------------

    registry = ToolRegistry()

    registry.register(calculator_tool)
    registry.register(search_tool)
    registry.register(file_reader_tool)

    # -----------------------------------------
    # Create Gemini LLM
    # -----------------------------------------

    llm = GeminiLLM()

    # -----------------------------------------
    # Create Agent
    # -----------------------------------------

    agent = Agent(
        llm=llm,
        registry=registry,
        max_iterations=5
    )

    # -----------------------------------------
    # Display available tools
    # -----------------------------------------

    print("Available tools:")

    for tool in registry.list_tools():
        print(f"- {tool.name}")

    # -----------------------------------------
    # FIRST QUESTION
    # -----------------------------------------

    question1 = """
Read data/company.txt and tell me:

1. What technologies does the company use?
2. What development methodology does it follow?
3. What does the AI Engineering team work on?
"""

    answer1 = agent.run(
        question1
    )

    print("\nFirst answer:")
    print(answer1)

    # -----------------------------------------
    # SECOND QUESTION
    # -----------------------------------------
    #
    # This question depends on the previous
    # conversation.
    #
    # The agent should use its memory.
    # -----------------------------------------

    question2 = """
Which technologies mentioned earlier are
related to AI Engineering?
"""

    answer2 = agent.run(
        question2
    )

    print("\nSecond answer:")
    print(answer2)


if __name__ == "__main__":
    main()