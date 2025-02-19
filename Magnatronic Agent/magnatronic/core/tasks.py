"""Celery Tasks Module for Magnatronic Multi-Agent System"""

from celery import Celery
from typing import Dict, Any
from ..agents.research_agent import ResearchAgent
from ..agents.creative_agent import CreativeAgent
from ..agents.knowledge_agent import KnowledgeAgent
from ..agents.monitoring_agent import MonitoringAgent

# Initialize Celery app
app = Celery('magnatronic')
app.config_from_object('magnatronic.core.celeryconfig')

# Agent instances
agents = {
    'research': ResearchAgent(),
    'creative': CreativeAgent(),
    'knowledge': KnowledgeAgent(),
    'monitoring': MonitoringAgent()
}

@app.task(name='agent.process_task')
async def process_task(task_data: Dict[str, Any], priority: int = 2) -> Dict[str, Any]:
    """Process a task using the appropriate agent.

    Args:
        task_data (Dict[str, Any]): Task data and parameters
        priority (int): Task priority level

    Returns:
        Dict[str, Any]: Task processing results
    """
    agent_type = task_data.get('agent_type')
    if agent_type not in agents:
        raise ValueError(f"Unknown agent type: {agent_type}")

    agent = agents[agent_type]
    result = await agent.process_task(task_data)

    # Notify monitoring agent of task completion
    monitoring_agent = agents['monitoring']
    await monitoring_agent.handle_message({
        'type': 'performance_update',
        'agent_id': agent.agent_id,
        'task_id': task_data.get('task_id'),
        'status': 'completed',
        'result': result
    })

    return result

@app.task(name='agent.health_check')
async def health_check() -> Dict[str, Any]:
    """Perform system health check using monitoring agent.

    Returns:
        Dict[str, Any]: Health check results
    """
    monitoring_agent = agents['monitoring']
    return await monitoring_agent.process_task({
        'type': 'system_health_check',
        'components': list(agents.keys())
    })