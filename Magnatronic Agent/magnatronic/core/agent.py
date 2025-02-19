"""Base Agent Module for Magnatronic Multi-Agent System"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from uuid import uuid4

class BaseAgent(ABC):
    """Base class for all Magnatronic agents"""

    def __init__(self, agent_id: Optional[str] = None, name: str = "base_agent"):
        """Initialize the base agent.

        Args:
            agent_id (str, optional): Unique identifier for the agent. Defaults to None.
            name (str, optional): Human-readable name for the agent. Defaults to "base_agent".
        """
        self.agent_id = agent_id or str(uuid4())
        self.name = name
        self.state: Dict[str, Any] = {}

    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task assigned to the agent.

        Args:
            task (Dict[str, Any]): Task data containing instructions and parameters.

        Returns:
            Dict[str, Any]: Result of the task processing.
        """
        pass

    @abstractmethod
    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming messages from other agents.

        Args:
            message (Dict[str, Any]): Message data from another agent.
        """
        pass

    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent.

        Returns:
            Dict[str, Any]: Current agent state.
        """
        return self.state

    def update_state(self, new_state: Dict[str, Any]) -> None:
        """Update the agent's state.

        Args:
            new_state (Dict[str, Any]): New state to update with.
        """
        self.state.update(new_state)