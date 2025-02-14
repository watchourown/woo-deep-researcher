# agents/hitl/configuration.py
import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional
from agents.hitl import prompts
from langchain_core.runnables import RunnableConfig

@dataclass(kw_only=True)
class Configuration:
    """
    The user-configurable fields for the assistant, including thread_id.
    This must match the names the checkpointer expects in config["configurable"].
    """
    # Make it a string if you want to allow arbitrary thread IDs like "abc123"
    # or keep it as int if you prefer numeric.
    thread_id: str = "default-thread"
    user_id: str = "1"
    model: str = "gpt-3.5-turbo"
    structured_output_model: str = "gpt-4"

    # prompts
    router_system_prompt: str = field(
        default=prompts.GENERATE_TASKS_SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt used for generating the tasks.",
        },
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        configurable = config.get("configurable", {}) if config else {}
        values: dict[str, Any] = {}
        for f in fields(cls):
            # e.g. thread_id => environment or config["configurable"].get("thread_id")
            env_val = os.environ.get(f.name.upper())
            cfg_val = configurable.get(f.name)
            # pick whichever is set (config is typically used if present)
            val = cfg_val if cfg_val is not None else env_val
            if val is not None:
                values[f.name] = val
        return cls(**values)