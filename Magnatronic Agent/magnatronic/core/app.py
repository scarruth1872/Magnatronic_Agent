from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import logging
from datetime import datetime
from collections import deque
from dataclasses import dataclass, asdict
import os

# Enhanced data models
class AgentMetrics(BaseModel):
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    task_completion_rate: float = 0.0
    response_time: float = 0.0
    uptime: float = 0.0

class Agent(BaseModel):
    id: str
    name: str
    type: str
    status: str = "idle"
    capabilities: List[str]
    metrics: AgentMetrics = AgentMetrics()
    last_heartbeat: Optional[datetime] = None
    performance_history: List[Dict[str, Any]] = []

# Enhanced in-memory storage with performance tracking
active_agents: Dict[str, Agent] = {}
task_queue: deque = deque(maxlen=1000)  # Limit queue size
websocket_connections: Dict[str, WebSocket] = {}
performance_history: Dict[str, List[Dict]] = {}
MAX_HISTORY_ENTRIES = 100  # Limit history entries per agent

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
    allow_origins=["http://localhost:7000", "http://localhost:7001", "http://localhost:8001"],  # Frontend URLs
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
@app.get("/api/system/metrics")
async def get_system_metrics():
    return {
        "agents": {
            "total": len(active_agents),
            "active": len([a for a in active_agents.values() if a.status != "offline"]),
            "busy": len([a for a in active_agents.values() if a.status == "busy"])
        },
        "tasks": {
            "total": len(task_queue),
            "pending": len([t for t in task_queue if t.status == "pending"]),
            "in_progress": len([t for t in task_queue if t.status == "in_progress"]),
            "completed": len([t for t in task_queue if t.status == "completed"])
        },
        "performance": {
            "avg_response_time": sum(a.metrics.response_time for a in active_agents.values()) / len(active_agents) if active_agents else 0,
            "avg_cpu_usage": sum(a.metrics.cpu_usage for a in active_agents.values()) / len(active_agents) if active_agents else 0,
            "avg_memory_usage": sum(a.metrics.memory_usage for a in active_agents.values()) / len(active_agents) if active_agents else 0
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/agents/{agent_id}/performance")
async def get_agent_performance(agent_id: str):
    if agent_id not in active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = active_agents[agent_id]
    history = performance_history.get(agent_id, [])
    
    return {
        "agent": agent.dict(),
        "current_metrics": agent.metrics.dict(),
        "performance_history": history,
        "task_stats": {
            "completed": len([t for t in task_queue if t.status == "completed" and t.assigned_to == agent_id]),
            "in_progress": len([t for t in task_queue if t.status == "in_progress" and t.assigned_to == agent_id]),
            "total_assigned": len([t for t in task_queue if t.assigned_to == agent_id])
        }
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "operational",
        "active_agents": len(active_agents),
        "pending_tasks": len([t for t in task_queue if t.status == "pending"]),
        "system_load": {
            "cpu": sum(a.metrics.cpu_usage for a in active_agents.values()) / len(active_agents) if active_agents else 0,
            "memory": sum(a.metrics.memory_usage for a in active_agents.values()) / len(active_agents) if active_agents else 0
        },
        "timestamp": datetime.now().isoformat()
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
    data: Optional[Dict[str, Any]] = None  # Add generic data field for enhanced checks

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
        elif request.action == "enhanced_checks":  # Placeholder for enhanced checks functionality
            result = "Enhanced checks not yet implemented"
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