from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any 
from core.agent import summary_bot
from logger import logger

app = FastAPI()

class RunRequest(BaseModel):
    initial_state : Dict[str,Any]

@app.post("/run/summarizer")
async def run_summarizer(request: RunRequest):
    logger.info("API request received: /run/summarizer")
    
    engine = summary_bot

    start_node = "split"

    try:
        final_state = await engine.run(start_node,request.initial_state)
        logger.info("API request completed successfully.")

    except Exception as e:
        logger.error(f"API Request failed: {e}")
        raise HTTPException(status_code = 500, detail = str(e))
    
    return{
        "status" : "Success",
        "final_summary" : final_state.get("current_summary"),
        "final_length" : final_state.get("current_length")
    }