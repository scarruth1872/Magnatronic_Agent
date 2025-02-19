"""Message Passing Interface for Magnatronic Multi-Agent System"""

from typing import Dict, Any, List, Optional
from redis import Redis
from json import dumps, loads

class MessageBroker:
    """Handles inter-agent communication using Redis as message broker"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """Initialize the message broker.

        Args:
            redis_url (str): Redis connection URL. Defaults to "redis://localhost:6379".
        """
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def send_message(self, sender_id: str, recipient_id: str, message: Dict[str, Any]) -> bool:
        """Send a message from one agent to another.

        Args:
            sender_id (str): ID of the sending agent
            recipient_id (str): ID of the receiving agent
            message (Dict[str, Any]): Message content

        Returns:
            bool: True if message was sent successfully
        """
        message_data = {
            "sender": sender_id,
            "content": message,
            "timestamp": self.redis.time()[0],
            "type": message.get("type", "general"),
            "priority": message.get("priority", "normal")
        }
        
        # Send performance metrics to monitoring agent
        if recipient_id == "monitoring_agent":
            if message.get("type") == "performance_update":
                self.redis.hset(
                    f"agent_metrics:{sender_id}",
                    mapping=message.get("metrics", {})
                )
        
        return bool(self.redis.rpush(f"messages:{recipient_id}", dumps(message_data)))

    async def get_messages(self, agent_id: str, count: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retrieve messages for a specific agent.

        Args:
            agent_id (str): ID of the agent to get messages for
            count (Optional[int]): Maximum number of messages to retrieve

        Returns:
            List[Dict[str, Any]]: List of messages
        """
        messages = []
        queue_key = f"messages:{agent_id}"
        
        # Get all messages if count is None, otherwise get specified number
        message_count = count or self.redis.llen(queue_key)
        
        for _ in range(message_count):
            message_data = self.redis.lpop(queue_key)
            if not message_data:
                break
            messages.append(loads(message_data))
            
        return messages

    def clear_messages(self, agent_id: str) -> None:
        """Clear all messages for a specific agent.

        Args:
            agent_id (str): ID of the agent whose messages should be cleared
        """
        self.redis.delete(f"messages:{agent_id}")