# agents/hitl/graph.py

from typing_extensions import Literal
from langgraph.types import interrupt, Command
from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from agents.hitl.state import HitlState, HitlStateInput, HitlStateOutput
from langgraph.checkpoint.mongodb import MongoDBSaver
from database.mongo import mongo_db, mongo_client

def ask_for_more_info(state: HitlState, config: RunnableConfig):
    """
    Just a placeholder node that 'prompts' the user to add more details.
    In real usage, you'd have the system produce a prompt or partial output.
    """
    
    # Here, we'd say something like: "We need more context about your request."
    # For demonstration, we'll just store a placeholder.
    # The user will provide real info in a follow-up route.
    print("Asking for more info.")
    feedback = interrupt("Please provide feedback:")
    print(feedback)
    return {"system_message": feedback}


def finalize_conversation(state: HitlState):
    """
    Once the user has provided additional info, finalize the conversation (simple).
    """

    # You might combine the user_provided_info with the system or run an LLM step.
    final_text = f"Conversation complete. Received extra info: {state.user_provided_info}"
    return {"final_result": final_text}


def route_logic(state: HitlState, config: RunnableConfig) -> Literal["finalize_conversation", "ask_for_more_info"]:
    """
    Decide if we still need info or if we can finalize.
    Suppose if 'user_provided_info' is empty, we go back to 'ask_for_more_info'.
    Otherwise, we finalize.
    """
    if state.user_provided_info:
        return "finalize_conversation"
    else:
        return "ask_for_more_info"


builder = StateGraph(state_schema=HitlState, input=HitlStateInput, output=HitlStateOutput)
builder.add_node("ask_for_more_info", ask_for_more_info)
builder.add_node("finalize_conversation", finalize_conversation)

# Flow
builder.add_edge(START, "ask_for_more_info")
builder.add_conditional_edges("ask_for_more_info", route_logic)
builder.add_edge("finalize_conversation", END)
# Set up memory

checkpointer = MongoDBSaver(
    client=mongo_client,
    db_name="woo_threads",
    checkpoint_collection_name="hitl_checkpoints",
    writes_collection_name="checkpoint_writes"
)
graph = builder.compile(checkpointer=checkpointer)