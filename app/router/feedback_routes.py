from fastapi import APIRouter
from pydantic import BaseModel
from agents.deep_researcher.configuration import Configuration
from agents.hitl.graph import graph
from agents.hitl.state import HitlStateInput
router = APIRouter()

class FeedbackData(BaseModel):
    thread_id: str
    feedback_text: str
    rating: int

@router.post("/feedback")
def post_feedback(data: FeedbackData):
    config = Configuration()
    # mongo_store = MongoStateStore(uri=config.mongodb_uri, db_name=config.mongodb_database)
    print(f"Received feedback: {data}")
    print(config)
    # mongo_store.save_feedback({
    #     "thread_id": data.thread_id,
    #     "feedback_text": data.feedback_text,
    #     "rating": data.rating
    # })

    return {"status": "feedback saved"}


@router.post("/startConvo")
def start_convo():
    thread_id = "demo-thread-1"

    # Initial call
    state_input = HitlStateInput(
        user_provided_info=""
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    # Invoke the graph
    result = graph.invoke(state_input, config=config)
    print(result)

    return {"status": "conversation started"}