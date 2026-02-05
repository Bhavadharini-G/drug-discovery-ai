from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.multi_agent import create_drug_discovery_crew
from dotenv import load_dotenv
import traceback

load_dotenv()

app = FastAPI()

class AnalyzeRequest(BaseModel):
    compound: str

@app.get("/")
def read_root():
    return {"message": "Drug Discovery AI API"}

@app.post("/analyze")
async def analyze_compound(request: AnalyzeRequest):
    try:
        crew = create_drug_discovery_crew()
        result = crew.kickoff(inputs={"compound": request.compound})
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
