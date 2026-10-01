# ReAct AI Agent from Scratch

A **ReAct-based AI Agent built from scratch using Python and Google Gemini API**, without using LangChain, LangGraph, AutoGen, CrewAI, or other agent frameworks.

The purpose of this project is to understand how modern AI agents work internally — including **LLM reasoning, tool calling, tool execution, scratchpad memory, conversation memory, error handling, and loop prevention**.

---

##  Project Overview

The agent follows the basic:

**Reason → Act → Observe → Reason → ... → Final Answer**

workflow.

For example, when a user asks:

> "Calculate 125 × 32 and read the company information from the file."

The agent can:

1. Understand the request.
2. Decide which tools are required.
3. Ask Gemini to call the required tools.
4. Execute the tools.
5. Observe the results.
6. Provide the results back to Gemini.
7. Continue the loop if more tools are required.
8. Generate the final answer.

---

##  Architecture

```text
                    User Question
                         │
                         ▼
                  ┌──────────────┐
                  │   AI Agent   │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Gemini LLM   │
                  └──────┬───────┘
                         │
                  Tool Call Request
                         │
                         ▼
                  ┌──────────────┐
                  │Tool Registry │
                  └──────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     Calculator       Search       File Reader
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
                    Tool Result
                         │
                         ▼
                    Observation
                         │
                         ▼
                    Scratchpad
                         │
                         ▼
                    Gemini LLM
                         │
                         ▼
                    Final Answer
