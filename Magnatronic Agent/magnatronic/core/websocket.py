from fastapi import WebSocket
from typing import List, Dict
from datetime import datetime
import json

class AgentWebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.agent_statuses: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_agent_status(self, agent_id: str, status: dict):
        self.agent_statuses[agent_id] = {
            **status,
            'last_updated': datetime.now().isoformat()
        }
        message = {
            'type': 'agent_status',
            'agent_id': agent_id,
            'data': self.agent_statuses[agent_id]
        }
        await self.broadcast(message)

    async def broadcast_system_metrics(self, metrics: dict):
        message = {
            'type': 'system_metrics',
            'data': metrics,
            'timestamp': datetime.now().isoformat()
        }
        await self.broadcast(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                await self.disconnect(connection)

manager = AgentWebSocketManager()