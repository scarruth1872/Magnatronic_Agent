"""Monitoring Agent Module for Magnatronic Multi-Agent System"""

import time
from typing import Dict, Any
from ..core.agent import BaseAgent
from ..core.communication import MessageBroker
from ..core.task_queue import TaskQueue, TaskPriority

class MonitoringAgent(BaseAgent):
    """Agent responsible for system performance monitoring, conflict detection, and resource management"""

    def __init__(self, agent_id: str = None):
        super().__init__(agent_id, name="monitoring_agent")
        self.message_broker = MessageBroker()
        self.task_queue = TaskQueue()
        self.state.update({
            "system_metrics": {},
            "active_alerts": [],
            "resource_usage": {},
            "agent_status": {},
            "healthcare_metrics": {},
            "security_alerts": [],
            "it_systems_status": {},
            "task_queue": [],
            "central_repository": {}
        })

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process monitoring tasks.

        Args:
            task (Dict[str, Any]): Task data containing monitoring parameters

        Returns:
            Dict[str, Any]: Monitoring results
        """
        task_type = task.get("type")
        if task_type == "performance_monitoring":
            return await self._monitor_performance(task)
        elif task_type == "conflict_detection":
            return await self._detect_conflicts(task)
        elif task_type == "resource_management":
            return await self._manage_resources(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming messages from other agents.

        Args:
            message (Dict[str, Any]): Message data from another agent
        """
        message_type = message.get("type")
        if message_type == "status_update":
            await self._handle_status_update(message)
        elif message_type == "alert":
            await self._handle_alert(message)

    async def monitor_it_systems(self) -> Dict[str, Any]:
        """Monitor IT systems performance and health.

        Returns:
            Dict[str, Any]: IT systems monitoring results
        """
        metrics = {}
        try:
            # Monitor network performance
            import socket
            metrics['network_connections'] = len(psutil.net_connections())
            metrics['network_io'] = psutil.net_io_counters()._asdict()

            # Monitor system services
            services = psutil.win_service_iter() if hasattr(psutil, 'win_service_iter') else []
            metrics['active_services'] = len(list(services))

            self.state['it_systems_status'] = metrics
            return {"status": "success", "metrics": metrics}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def monitor_healthcare_systems(self) -> Dict[str, Any]:
        """Monitor healthcare systems and patient data.

        Returns:
            Dict[str, Any]: Healthcare monitoring results
        """
        metrics = {}
        try:
            # Simulate monitoring patient vital signs
            metrics['active_patients'] = len(self.state.get('healthcare_metrics', {}))
            metrics['critical_alerts'] = sum(1 for alert in self.state['active_alerts'] 
                                          if alert.get('priority') == 'critical' and 
                                          alert.get('type') == 'healthcare')

            self.state['healthcare_metrics'] = metrics
            return {"status": "success", "metrics": metrics}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def monitor_security(self) -> Dict[str, Any]:
        """Monitor security threats and system vulnerabilities.

        Returns:
            Dict[str, Any]: Security monitoring results
        """
        metrics = {}
        try:
            # Monitor security-related metrics
            metrics['failed_login_attempts'] = len([alert for alert in self.state['security_alerts'] 
                                                  if alert.get('type') == 'failed_login'])
            metrics['suspicious_activities'] = len([alert for alert in self.state['security_alerts'] 
                                                  if alert.get('type') == 'suspicious_activity'])

            # Update security alerts
            self.state['security_alerts'] = [alert for alert in self.state['security_alerts'] 
                                           if time.time() - alert.get('timestamp', 0) < 3600]  # Keep last hour

            return {"status": "success", "metrics": metrics}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def update_central_repository(self, data: Dict[str, Any]) -> None:
        """Update the central repository with new information.

        Args:
            data (Dict[str, Any]): Data to be added to the central repository
        """
        try:
            self.state['central_repository'].update(data)
        except Exception as e:
            self.state['active_alerts'].append({
                "type": "repository_error",
                "message": f"Failed to update central repository: {str(e)}",
                "timestamp": time.time()
            })

    async def delegate_task(self, task: Dict[str, Any]) -> None:
        """Delegate tasks to appropriate agents.

        Args:
            task (Dict[str, Any]): Task to be delegated
        """
        try:
            self.state['task_queue'].append(task)
            # Implement task delegation logic here
            # This would involve communicating with other agents
        except Exception as e:
            self.state['active_alerts'].append({
                "type": "task_delegation_error",
                "message": f"Failed to delegate task: {str(e)}",
                "timestamp": time.time()
            })

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a monitoring task.

        Args:
            task (Dict[str, Any]): Task data containing monitoring parameters

        Returns:
            Dict[str, Any]: Monitoring results
        """
        task_type = task.get("type")
        if task_type == "performance_monitoring":
            return await self._monitor_performance(task)
        elif task_type == "conflict_detection":
            return await self._detect_conflicts(task)
        elif task_type == "resource_management":
            return await self._manage_resources(task)
        else:
            raise ValueError(f"Unknown task type: {task_type}")

    async def handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming messages from other agents.

        Args:
            message (Dict[str, Any]): Message data from another agent
        """
        message_type = message.get("type")
        if message_type == "status_update":
            await self._handle_status_update(message)
        elif message_type == "alert":
            await self._handle_alert(message)

    async def _monitor_performance(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor system performance metrics.

        Args:
            task (Dict[str, Any]): Performance monitoring parameters

        Returns:
            Dict[str, Any]: Performance monitoring results
        """
        metrics = {}
        
        # Monitor CPU and memory usage
        try:
            import psutil
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['memory_percent'] = psutil.virtual_memory().percent
            metrics['disk_usage'] = psutil.disk_usage('/').percent
            
            # Monitor per-agent performance
            for agent_id, status in self.state['agent_status'].items():
                process = psutil.Process(status.get('pid'))
                metrics[f'agent_{agent_id}'] = {
                    'cpu_percent': process.cpu_percent(),
                    'memory_usage': process.memory_info().rss / 1024 / 1024,  # MB
                    'request_count': status.get('request_count', 0),
                    'error_count': status.get('error_count', 0),
                    'avg_processing_time': status.get('avg_processing_time', 0)
                }
                
        except ImportError:
            metrics['error'] = 'psutil library not available'

        # Monitor agent performance
        metrics['active_agents'] = len(self.state['agent_status'])
        metrics['alert_count'] = len(self.state['active_alerts'])
        metrics['nlp_queue_size'] = len(self.state.get('nlp_tasks', []))
        
        # Update system metrics in state
        self.state['system_metrics'] = metrics
        
        return {
            "status": "success",
            "metrics": metrics,
            "timestamp": time.time()
        }

    async def _detect_conflicts(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Detect and analyze conflicts between agents.

        Args:
            task (Dict[str, Any]): Conflict detection parameters

        Returns:
            Dict[str, Any]: Conflict detection results
        """
        conflicts = []
        
        # Check for resource conflicts
        if self.state['resource_usage'].get('memory', {}).get('percent', 0) > 85:
            conflicts.append({
                'type': 'resource_conflict',
                'severity': 'warning',
                'message': 'High memory usage may cause agent conflicts'
            })
            
        # Check for task conflicts
        agent_tasks = {}
        for agent_id, status in self.state['agent_status'].items():
            current_task = status.get('current_task')
            if current_task:
                if current_task in agent_tasks:
                    conflicts.append({
                        'type': 'task_conflict',
                        'severity': 'error',
                        'message': f'Task {current_task} assigned to multiple agents',
                        'agents': [agent_id, agent_tasks[current_task]]
                    })
                agent_tasks[current_task] = agent_id
                
        return {
            'status': 'success',
            'conflicts': conflicts,
            'timestamp': time.time()
        }

    async def _manage_resources(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Manage system resources and optimize allocation.

        Args:
            task (Dict[str, Any]): Resource management parameters

        Returns:
            Dict[str, Any]: Resource management results
        """
        try:
            import psutil
            
            # Get current resource usage
            cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Update resource usage state
            self.state['resource_usage'] = {
                'cpu': {
                    'total_percent': sum(cpu_usage) / len(cpu_usage),
                    'per_cpu': cpu_usage
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': disk.percent
                },
                'timestamp': time.time()
            }
            
            # Basic resource optimization logic
            recommendations = []
            if memory.percent > 90:
                recommendations.append("High memory usage detected - consider freeing up memory")
            if disk.percent > 90:
                recommendations.append("Low disk space - cleanup recommended")
            
            return {
                "status": "success",
                "resource_usage": self.state['resource_usage'],
                "recommendations": recommendations
            }
            
        except ImportError:
            return {
                "status": "error",
                "message": "Required monitoring libraries not available"
            }

    async def _handle_status_update(self, message: Dict[str, Any]) -> None:
        """Handle status updates from other agents.

        Args:
            message (Dict[str, Any]): Status update message
        """
        # TODO: Implement status update handling
        pass

    async def _handle_alert(self, message: Dict[str, Any]) -> None:
        """Handle alert messages from other agents.

        Args:
            message (Dict[str, Any]): Alert message containing severity and details
        """
        alert_data = {
            'source': message.get('source', 'unknown'),
            'severity': message.get('severity', 'info'),
            'message': message.get('message', ''),
            'timestamp': time.time(),
            'context': message.get('context', {})
        }
        
        # Add alert to active alerts with expiration
        alert_data['expires_at'] = time.time() + (
            3600 if alert_data['severity'] in ['critical', 'error'] else 1800
        )
        self.state['active_alerts'].append(alert_data)
        
        # Clean expired alerts
        self._clean_expired_alerts()
        
        # Process alert based on severity
        await self._process_alert(alert_data)