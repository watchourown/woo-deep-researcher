from fastapi import APIRouter
from pydantic import BaseModel
from agents.deep_researcher.configuration import Configuration

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