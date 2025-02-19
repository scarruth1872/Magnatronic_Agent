from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Dict, Any
import time
from datetime import datetime
import os

# Initialize templates
templates = Jinja2Templates(directory="magnatronic/templates")

# Initialize FastAPI app with Matrix Grimoire styling for responses
app = FastAPI(
    title="Matrix Grimoire API",
    description="Backend API for the Matrix Grimoire Multi-Agent System",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:7000", "http://localhost:7001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directories
app.mount("/public", StaticFiles(directory="public"), name="public")
app.mount("/magnatronic", StaticFiles(directory="magnatronic"), name="magnatronic")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Get system metrics
    active_agents = 5  # Example value - implement actual agent counting
    response_time = 42  # Example value - implement actual response time measurement
    
    return templates.TemplateResponse(
        "base.html",
        {
            "request": request,
            "active_agents": active_agents,
            "response_time": response_time
        }
    )

# Custom error styling following Matrix Grimoire aesthetic
class MatrixError(BaseModel):
    error: str
    timestamp: str
    code: int
    details: Optional[Dict[str, Any]] = None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error = MatrixError(
        error=exc.detail,
        timestamp=datetime.now().isoformat(),
        code=exc.status_code,
        details={"path": request.url.path}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error.dict()
    )



# Favicon endpoint handler
@app.get("/favicon.ico")
async def favicon():
    return FileResponse('public/favicon.ico')

# Health check endpoint with styled response
@app.get("/api/health")
async def health_check():
    return {
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "version": app.version,
        "environment": "development"
    }

# NLP Metrics endpoint with Matrix Grimoire styling
@app.get("/api/nlp/metrics")
async def get_nlp_metrics():
    return {
        "metrics": {
            "requestCount": 100,
            "errorCount": 5,
            "avgProcessingTime": 0.5
        },
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

# NLP Processing endpoint
class NLPRequest(BaseModel):
    action: str
    text: str
    targetLanguage: Optional[str] = None

@app.post("/api/nlp")
async def process_nlp(request: NLPRequest):
    try:
        # Mock processing based on action
        if request.action == "translate":
            result = f"Translated text to {request.targetLanguage}"
        elif request.action == "analyze":
            result = "Analysis results for the text"
        elif request.action == "summarize":
            result = "Summary of the text"
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported action: {request.action}")
        
        return {
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "processingTime": 0.5
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)