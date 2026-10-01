from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentStep:
    tool_name: str
    arguments: dict[str, Any]
    observation: str


@dataclass
class Scratchpad:
    steps: list[AgentStep] = field(default_factory=list)

    def add_step(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        observation: str
    ):
        step = AgentStep(
            tool_name=tool_name,
            arguments=arguments,
            observation=observation
        )

        self.steps.append(step)

    def render(self) -> str:
        if not self.steps:
            return "No previous tool calls."

        lines = []

        for i, step in enumerate(self.steps, start=1):
            lines.append(
                f"Step {i}\n"
                f"Action: {step.tool_name}\n"
                f"Arguments: {step.arguments}\n"
                f"Observation: {step.observation}"
            )

        return "\n\n".join(lines)

    def has_seen_action(
        self,
        tool_name: str,
        arguments: dict[str, Any]
    ) -> bool:

        for step in self.steps:

            if (
                step.tool_name == tool_name
                and step.arguments == arguments
            ):
                return True

        return False

    def clear(self):
        self.steps.clear()