# app/routers/deep_researcher.py
from fastapi import APIRouter
from agents.deep_researcher.state import SummaryStateInput
from agents.deep_researcher.configuration import Configuration
from agents.deep_researcher.graph import graph  # Assuming you moved the graph-building code there
from langchain_core.runnables import RunnableConfig

router = APIRouter()

@router.post("/deep-research")
async def run_deep_research(input_data: SummaryStateInput):
    """
    Invoke the 'deep researcher' graph to perform web-based research and summarization.
    """
    # Build a configuration object (customize as needed).
    config = RunnableConfig(configurable={
        "local_llm": "deepseek-r1:14b",
        "ollama_base_url": "http://localhost:11434",
        "max_web_research_loops": 2
    })

    # 🟢 Await the async graph invocation
    final_state = await graph.ainvoke(input_data, config)

    # Return the final summary
    return {
       "running_summary": final_state
    }