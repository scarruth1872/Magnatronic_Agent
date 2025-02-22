"""Load Balancer Module for Magnatronic Multi-Agent System"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from .monitoring import MonitoringSystem

@dataclass
class AgentLoad:
    """Data class for storing agent load information"""
    agent_id: str
    cpu_usage: float
    memory_usage: float
    task_count: int
    last_task_timestamp: Optional[datetime]
    capabilities: List[str]

class LoadBalancer:
    """Handles task distribution and load balancing between agents"""

    def __init__(self, monitoring_system: MonitoringSystem):
        """Initialize the load balancer.

        Args:
            monitoring_system (MonitoringSystem): Reference to the monitoring system
        """
        self.monitoring = monitoring_system
        self.agent_loads: Dict[str, AgentLoad] = {}
        self.load_threshold = 0.8  # 80% load threshold

    async def update_agent_load(self, agent_id: str, capabilities: List[str]) -> None:
        """Update load information for an agent.

        Args:
            agent_id (str): ID of the agent
            capabilities (List[str]): List of agent capabilities
        """
        metrics = await self.monitoring.get_agent_metrics(agent_id)
        if metrics:
            current = metrics['current']
            self.agent_loads[agent_id] = AgentLoad(
                agent_id=agent_id,
                cpu_usage=current['cpu_usage'],
                memory_usage=current['memory_usage'],
                task_count=0,  # Reset on update
                last_task_timestamp=datetime.now(),
                capabilities=capabilities
            )

    def get_agent_load(self, agent_id: str) -> Optional[AgentLoad]:
        """Get current load information for an agent.

        Args:
            agent_id (str): ID of the agent

        Returns:
            Optional[AgentLoad]: Agent load information if available
        """
        return self.agent_loads.get(agent_id)

    async def find_best_agent(self, required_capabilities: List[str], exclude_agents: List[str] = None) -> Optional[str]:
        """Find the most suitable agent for a task based on load and capabilities.

        Args:
            required_capabilities (List[str]): Capabilities required for the task
            exclude_agents (List[str], optional): Agents to exclude from consideration

        Returns:
            Optional[str]: ID of the best suited agent, if any
        """
        exclude_agents = exclude_agents or []
        candidates: List[Tuple[str, float]] = []

        for agent_id, load in self.agent_loads.items():
            if agent_id in exclude_agents:
                continue

            # Check if agent has all required capabilities
            if not all(cap in load.capabilities for cap in required_capabilities):
                continue

            # Calculate load score (lower is better)
            load_score = (
                load.cpu_usage * 0.4 +  # 40% weight to CPU usage
                load.memory_usage * 0.3 +  # 30% weight to memory usage
                (load.task_count / 10) * 0.3  # 30% weight to task count (normalized)
            )

            if load_score < self.load_threshold:
                candidates.append((agent_id, load_score))

        if not candidates:
            return None

        # Return agent with lowest load score
        return min(candidates, key=lambda x: x[1])[0]

    async def assign_task(self, agent_id: str) -> bool:
        """Record task assignment to an agent.

        Args:
            agent_id (str): ID of the agent

        Returns:
            bool: True if assignment was recorded successfully
        """
        if agent_id in self.agent_loads:
            load = self.agent_loads[agent_id]
            load.task_count += 1
            load.last_task_timestamp = datetime.now()
            return True
        return False

    async def complete_task(self, agent_id: str) -> bool:
        """Record task completion for an agent.

        Args:
            agent_id (str): ID of the agent

        Returns:
            bool: True if completion was recorded successfully
        """
        if agent_id in self.agent_loads:
            load = self.agent_loads[agent_id]
            if load.task_count > 0:
                load.task_count -= 1
            return True
        return False

    def get_system_load_distribution(self) -> Dict[str, float]:
        """Get current load distribution across all agents.

        Returns:
            Dict[str, float]: Agent IDs mapped to their load percentages
        """
        return {
            agent_id: (load.cpu_usage * 0.4 + load.memory_usage * 0.3 + 
                      (load.task_count / 10) * 0.3)
            for agent_id, load in self.agent_loads.items()
        }