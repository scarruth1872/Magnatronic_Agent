"""Celery Configuration for Magnatronic Multi-Agent System"""

# Broker settings
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# Task settings
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'

# Task execution settings
task_acks_late = True
task_reject_on_worker_lost = True
task_track_started = True

# Queue settings
task_default_queue = 'default'
task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'agent_tasks': {
        'exchange': 'agent_tasks',
        'routing_key': 'agent_tasks',
    }
}

# Task routing
task_routes = {
    'agent.*': {'queue': 'agent_tasks'}
}

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000

# Task result settings
result_expires = 3600  # Results expire after 1 hour
task_ignore_result = False

# Security settings
security_key = None  # Set this in production

# Logging settings
worker_redirect_stdouts = False
worker_redirect_stdouts_level = 'INFO'