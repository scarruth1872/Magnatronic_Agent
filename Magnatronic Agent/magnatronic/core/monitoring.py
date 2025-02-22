"""Monitoring System for Magnatronic Multi-Agent System"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import psutil
import asyncio
from dataclasses import dataclass
from collections import deque

@dataclass
class AgentMetrics:
    """Data class for storing agent performance metrics"""
    cpu_usage: float
    memory_usage: float
    task_completion_rate: float
    response_time: float
    uptime: float
    last_heartbeat: datetime

class MonitoringSystem:
    """Handles system-wide monitoring and metrics collection"""

    def __init__(self, history_size: int = 1000):
        """Initialize the monitoring system.

        Args:
            history_size (int): Maximum number of historical metrics to store
        """
        self.metrics_history: Dict[str, deque] = {}
        self.history_size = history_size
        self.system_metrics: Dict[str, Any] = {}
        self.agent_metrics: Dict[str, AgentMetrics] = {}

    async def update_agent_metrics(self, agent_id: str, metrics: Dict[str, float]) -> None:
        """Update metrics for a specific agent.

        Args:
            agent_id (str): ID of the agent
            metrics (Dict[str, float]): New metrics data
        """
        if agent_id not in self.metrics_history:
            self.metrics_history[agent_id] = deque(maxlen=self.history_size)

        current_time = datetime.now()
        agent_metrics = AgentMetrics(
            cpu_usage=metrics.get('cpu_usage', 0.0),
            memory_usage=metrics.get('memory_usage', 0.0),
            task_completion_rate=metrics.get('task_completion_rate', 0.0),
            response_time=metrics.get('response_time', 0.0),
            uptime=metrics.get('uptime', 0.0),
            last_heartbeat=current_time
        )

        self.agent_metrics[agent_id] = agent_metrics
        self.metrics_history[agent_id].append({
            'timestamp': current_time.isoformat(),
            'metrics': metrics
        })

    async def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current metrics for a specific agent.

        Args:
            agent_id (str): ID of the agent

        Returns:
            Optional[Dict[str, Any]]: Agent metrics if available
        """
        if agent_id in self.agent_metrics:
            metrics = self.agent_metrics[agent_id]
            return {
                'current': metrics.__dict__,
                'history': list(self.metrics_history[agent_id])
            }
        return None

    async def update_system_metrics(self) -> None:
        """Update system-wide performance metrics."""
        self.system_metrics = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': dict(psutil.net_io_counters()._asdict()),
            'timestamp': datetime.now().isoformat()
        }

    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get current system-wide metrics.

        Returns:
            Dict[str, Any]: System metrics
        """
        return self.system_metrics

    async def start_monitoring(self) -> None:
        """Start continuous system monitoring."""
        while True:
            await self.update_system_metrics()
            await asyncio.sleep(60)  # Update every minute

    def get_agent_status(self, agent_id: str) -> str:
        """Get the current status of an agent based on its metrics.

        Args:
            agent_id (str): ID of the agent

        Returns:
            str: Agent status (active, inactive, or unknown)
        """
        if agent_id in self.agent_metrics:
            metrics = self.agent_metrics[agent_id]
            time_since_heartbeat = (datetime.now() - metrics.last_heartbeat).total_seconds()
            
            if time_since_heartbeat > 300:  # 5 minutes threshold
                return 'inactive'
            return 'active'
        return 'unknown'

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status.

        Returns:
            Dict[str, Any]: System health information
        """
        active_agents = sum(1 for status in 
            [self.get_agent_status(agent_id) for agent_id in self.agent_metrics]
            if status == 'active')

        return {
            'status': 'healthy' if active_agents > 0 else 'degraded',
            'active_agents': active_agents,
            'total_agents': len(self.agent_metrics),
            'system_load': self.system_metrics.get('cpu_percent', 0),
            'memory_usage': self.system_metrics.get('memory_percent', 0),
            'timestamp': datetime.now().isoformat()
        }