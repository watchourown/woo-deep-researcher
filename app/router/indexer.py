# app/router/deep_researcher.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
# from agents.deep_researcher.graph import index_workflow, query_workflow

router = APIRouter()
logger = logging.getLogger(__name__)

# Define request payloads
class IndexPayload(BaseModel):
    text: str

class QueryPayload(BaseModel):
    query: str

@router.post("/index")
async def index(payload: IndexPayload):
    logger.info("Received index request")
    try:
        # result = index_workflow(payload.text)
        logger.info("Indexing workflow completed")
        return {"status": "success", "result": "result"}
    except Exception as e:
        logger.error("Error in indexing: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query(payload: QueryPayload):
    logger.info("Received query request")
    try:
        # result = query_workflow(payload.query)
        logger.info("Query workflow completed")
        return {"status": "success", "result": "result"}
    except Exception as e:
        logger.error("Error in querying: %s", e)
        raise HTTPException(status_code=500, detail=str(e))