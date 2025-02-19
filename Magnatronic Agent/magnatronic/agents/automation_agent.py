from magnatronic.core.agent import Agent
from magnatronic.core.tasks import TaskQueue
from datetime import datetime
import schedule
import time

class AutomationAgent(Agent):
    def __init__(self):
        super().__init__(name='automation')
        self.task_queue = TaskQueue()
        self.scheduler = schedule.Scheduler()

    def automate_task(self, task_function, *args, **kwargs):
        """Automate a repetitive task by scheduling it for execution"""
        try:
            return self.task_queue.enqueue(task_function, *args, **kwargs)
        except Exception as e:
            self.log.error(f"Error automating task: {str(e)}")
            return None

    def optimize_workflow(self, workflow_steps):
        """Optimize a workflow by organizing and executing steps efficiently"""
        optimized_steps = []
        for step in workflow_steps:
            # Add dependency checking and parallel execution where possible
            if step.get('parallel', False):
                self.task_queue.enqueue_parallel(step['function'], *step.get('args', []))
            else:
                optimized_steps.append(step)
        
        return self.execute_workflow(optimized_steps)

    def execute_workflow(self, workflow_steps):
        """Execute a series of workflow steps in sequence"""
        results = []
        for step in workflow_steps:
            try:
                result = step['function'](*step.get('args', []))
                results.append({
                    'step': step['name'],
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'step': step['name'],
                    'status': 'error',
                    'error': str(e)
                })
        return results

    def schedule_task(self, task_function, schedule_type, *args, **kwargs):
        """Schedule a task for execution at specified times"""
        if schedule_type.get('type') == 'interval':
            self.scheduler.every(schedule_type['value']).seconds.do(
                task_function, *args, **kwargs)
        elif schedule_type.get('type') == 'daily':
            self.scheduler.every().day.at(schedule_type['time']).do(
                task_function, *args, **kwargs)
        elif schedule_type.get('type') == 'weekly':
            self.scheduler.every().week.at(schedule_type['time']).do(
                task_function, *args, **kwargs)

    def set_reminder(self, message, reminder_time):
        """Set a reminder for a specific time"""
        def reminder_task():
            self.log.info(f"Reminder: {message}")
            # Implement notification system here

        reminder_datetime = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M')
        self.schedule_task(reminder_task, {
            'type': 'once',
            'time': reminder_datetime.strftime('%H:%M')
        })

    def run(self):
        """Run the automation agent's scheduler"""
        while True:
            self.scheduler.run_pending()
            time.sleep(1)