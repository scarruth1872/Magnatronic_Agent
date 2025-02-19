"""Task Queue System for Magnatronic Multi-Agent System"""

from typing import Dict, Any, List, Optional
from celery import Celery
from datetime import datetime
from enum import Enum

class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskQueue:
    """Handles task allocation and load balancing between agents"""

    def __init__(self, broker_url: str = "redis://localhost:6379"):
        """Initialize the task queue.

        Args:
            broker_url (str): Celery broker URL. Defaults to "redis://localhost:6379".
        """
        self.app = Celery('magnatronic', broker=broker_url)
        self.app.conf.task_routes = {
            'agent.*': {'queue': 'agent_tasks'}
        }

    async def submit_task(self, task_data: Dict[str, Any], priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Submit a task to the queue.

        Args:
            task_data (Dict[str, Any]): Task data and parameters
            priority (TaskPriority): Task priority level

        Returns:
            str: Task ID
        """
        task = self.app.send_task(
            'agent.process_task',
            args=[task_data],
            kwargs={'priority': priority.value},
            queue='agent_tasks'
        )
        return task.id

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task.

        Args:
            task_id (str): ID of the task to check

        Returns:
            Dict[str, Any]: Task status information
        """
        task = self.app.AsyncResult(task_id)
        return {
            'task_id': task_id,
            'status': task.status,
            'result': task.result if task.ready() else None,
            'timestamp': datetime.now().isoformat()
        }

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or running task.

        Args:
            task_id (str): ID of the task to cancel

        Returns:
            bool: True if task was cancelled successfully
        """
        task = self.app.AsyncResult(task_id)
        return task.revoke(terminate=True)

    async def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all tasks, optionally filtered by status.

        Args:
            status (Optional[str]): Filter tasks by status

        Returns:
            List[Dict[str, Any]]: List of task information
        """
        inspector = self.app.control.inspect()
        active = inspector.active() or {}
        reserved = inspector.reserved() or {}
        scheduled = inspector.scheduled() or {}

        tasks = []
        for worker, worker_tasks in active.items():
            for task in worker_tasks:
                if not status or task['status'] == status:
                    tasks.append({
                        'task_id': task['id'],
                        'status': 'active',
                        'worker': worker,
                        'name': task['name'],
                        'args': task['args'],
                        'kwargs': task['kwargs']
                    })

        # Add reserved and scheduled tasks
        for worker_tasks in [reserved, scheduled]:
            for worker, tasks_list in worker_tasks.items():
                for task in tasks_list:
                    if not status or task['status'] == status:
                        tasks.append({
                            'task_id': task['id'],
                            'status': 'pending',
                            'worker': worker,
                            'name': task['name'],
                            'args': task['args'],
                            'kwargs': task['kwargs']
                        })

        return tasks