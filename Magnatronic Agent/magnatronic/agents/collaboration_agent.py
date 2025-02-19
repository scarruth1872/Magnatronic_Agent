from magnatronic.core.agent import Agent
from magnatronic.core.tasks import task
from datetime import datetime

class CollaborationAgent(Agent):
    def __init__(self):
        super().__init__(name='collaboration')
        self.team_spaces = {}
        self.projects = {}
        self.shared_documents = {}

    @task
    def create_team_space(self, team_id, team_name, members):
        """Create a new team collaboration space."""
        if team_id not in self.team_spaces:
            self.team_spaces[team_id] = {
                'name': team_name,
                'members': members,
                'channels': [],
                'created_at': datetime.now().isoformat()
            }
        return self.team_spaces[team_id]

    @task
    def create_project(self, team_id, project_data):
        """Create a new project within a team space."""
        if team_id not in self.team_spaces:
            return None

        project_id = project_data.get('id')
        if project_id not in self.projects:
            self.projects[project_id] = {
                'team_id': team_id,
                'name': project_data.get('name'),
                'description': project_data.get('description'),
                'tasks': [],
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
        return self.projects[project_id]

    @task
    def update_project_task(self, project_id, task_data):
        """Update or create a task within a project."""
        if project_id not in self.projects:
            return None

        task_id = task_data.get('id')
        existing_tasks = [t for t in self.projects[project_id]['tasks'] if t['id'] == task_id]
        
        if existing_tasks:
            existing_tasks[0].update(task_data)
            task = existing_tasks[0]
        else:
            task = {
                'id': task_id,
                'title': task_data.get('title'),
                'description': task_data.get('description'),
                'assignee': task_data.get('assignee'),
                'status': task_data.get('status', 'todo'),
                'created_at': datetime.now().isoformat()
            }
            self.projects[project_id]['tasks'].append(task)
        
        return task

    @task
    def share_document(self, team_id, document_data):
        """Share a document within a team space."""
        if team_id not in self.team_spaces:
            return None

        doc_id = document_data.get('id')
        if doc_id not in self.shared_documents:
            self.shared_documents[doc_id] = {
                'team_id': team_id,
                'name': document_data.get('name'),
                'type': document_data.get('type'),
                'url': document_data.get('url'),
                'permissions': document_data.get('permissions', []),
                'shared_at': datetime.now().isoformat()
            }
        return self.shared_documents[doc_id]

    @task
    def get_team_documents(self, team_id):
        """Retrieve all documents shared within a team space."""
        if team_id not in self.team_spaces:
            return []
        
        return [
            doc for doc in self.shared_documents.values()
            if doc['team_id'] == team_id
        ]

    @task
    def get_project_tasks(self, project_id):
        """Retrieve all tasks for a specific project."""
        if project_id not in self.projects:
            return []
        
        return self.projects[project_id]['tasks']