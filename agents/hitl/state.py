# agents/hitl/state.py

from dataclasses import dataclass, field
from typing import Optional
from typing_extensions import TypedDict

@dataclass
class HitlState:
    # Internal working state for the conversation
    user_provided_info: Optional[str] = None
    system_message: Optional[str] = None
    final_result: Optional[str] = None

@dataclass
class HitlStateInput(TypedDict):
    # Input from user
    user_provided_info: Optional[str]

@dataclass
class HitlStateOutput(TypedDict):
    # Output from graph
    final_result: Optional[str]