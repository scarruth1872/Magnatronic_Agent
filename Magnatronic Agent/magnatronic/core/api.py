from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from .websocket import manager
from datetime import datetime

app = FastAPI(title="Magnatronic Agent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data for testing
mock_agents = [
    {
        "id": "agent-001",
        "name": "Research Agent",
        "type": "research",
        "status": "active",
        "metrics": {
            "cpu_usage": 45,
            "memory_usage": 134217728,  # 128MB in bytes
            "task_completion_rate": 92,
            "response_time": 0.8
        },
        "tasks": ["Analyzing market trends", "Gathering competitor data"]
    },
    {
        "id": "agent-002",
        "name": "Creative Agent",
        "type": "creative",
        "status": "active",
        "metrics": {
            "cpu_usage": 35,
            "memory_usage": 100663296,  # 96MB in bytes
            "task_completion_rate": 88,
            "response_time": 1.2
        },
        "tasks": ["Generating content ideas", "Writing blog posts"]
    }
]

@app.get("/")
async def root():
    return {"message": "Magnatronic Agent API is running"}

@app.get("/api/agents", response_model=List[Dict])
async def get_agents():
    return mock_agents

@app.get("/api/system/metrics")
async def get_system_metrics():
    metrics = {
        "agents": mock_agents,
        "system_status": "healthy",
        "total_agents": len(mock_agents),
        "active_agents": sum(1 for agent in mock_agents if agent["status"] == "active"),
        "system_load": {
            "cpu": 45,
            "memory": 256000000,  # 256MB in bytes
            "network": "stable"
        },
        "timestamp": datetime.now().isoformat()
    }
    await manager.broadcast_system_metrics(metrics)
    return metrics

@app.get("/api/agents/{agent_id}/performance")
async def get_agent_performance(agent_id: str):
    # Find the agent in mock data
    agent = next((a for a in mock_agents if a["id"] == agent_id), None)
    if not agent:
        return {"error": "Agent not found"}
    
    # Return performance data
    return {
        "agent": agent,
        "task_stats": {
            "total_assigned": 150,
            "completed": 138,
            "in_progress": 10,
            "failed": 2
        },
        "current_metrics": {
            "task_completion_rate": agent["metrics"]["task_completion_rate"],
            "response_time": agent["metrics"]["response_time"],
            "cpu_usage": agent["metrics"]["cpu_usage"],
            "memory_usage": agent["metrics"]["memory_usage"]
        }
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except:
        manager.disconnect(websocket)