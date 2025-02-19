from magnatronic.core.agent import Agent
from magnatronic.core.tasks import TaskQueue
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from threading import Thread

class DataVisualizationAgent(Agent):
    def __init__(self):
        super().__init__(name='data_visualization')
        self.task_queue = TaskQueue()
        self.app = Dash(__name__)
        self.dashboards = {}

    def create_visualization(self, data, viz_type, **kwargs):
        """Create a visualization based on the provided data and type"""
        try:
            if isinstance(data, dict):
                data = pd.DataFrame(data)
            
            if viz_type == 'line':
                fig = px.line(data, **kwargs)
            elif viz_type == 'bar':
                fig = px.bar(data, **kwargs)
            elif viz_type == 'scatter':
                fig = px.scatter(data, **kwargs)
            elif viz_type == 'pie':
                fig = px.pie(data, **kwargs)
            else:
                raise ValueError(f"Unsupported visualization type: {viz_type}")
            
            return fig
        except Exception as e:
            self.log.error(f"Error creating visualization: {str(e)}")
            return None

    def create_dashboard(self, dashboard_id, layout):
        """Create an interactive dashboard with the specified layout"""
        try:
            self.dashboards[dashboard_id] = layout
            self.app.layout = html.Div([
                html.H1(dashboard_id),
                *layout
            ])
            return True
        except Exception as e:
            self.log.error(f"Error creating dashboard: {str(e)}")
            return False

    def update_visualization(self, dashboard_id, component_id, new_data):
        """Update a visualization in real-time"""
        @self.app.callback(
            Output(component_id, 'figure'),
            Input('interval-component', 'n_intervals')
        )
        def update(n):
            try:
                return self.create_visualization(new_data, 'line')
            except Exception as e:
                self.log.error(f"Error updating visualization: {str(e)}")
                return go.Figure()

    def add_real_time_component(self, dashboard_id, interval_ms=1000):
        """Add real-time update capability to a dashboard"""
        if dashboard_id in self.dashboards:
            self.dashboards[dashboard_id].append(
                dcc.Interval(
                    id='interval-component',
                    interval=interval_ms,
                    n_intervals=0
                )
            )

    def run_dashboard(self, host='localhost', port=7000):
        """Run the dashboard server"""
        def run():
            self.app.run_server(host=host, port=port)

        dashboard_thread = Thread(target=run)
        dashboard_thread.daemon = True
        dashboard_thread.start()

    def run(self):
        """Run the data visualization agent"""
        self.run_dashboard()