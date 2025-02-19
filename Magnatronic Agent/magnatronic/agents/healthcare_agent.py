from magnatronic.core.agent import Agent
from magnatronic.core.communication import MessageBroker
from magnatronic.core.task_queue import TaskQueue, TaskPriority
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

class HealthcareAgent(Agent):
    def __init__(self, agent_id: str = None):
        super().__init__(agent_id, name="healthcare_agent")
        self.state.update({
            "patient_vitals": {},
            "medical_research_data": {},
            "appointments": [],
            "patient_records": {},
            "vital_thresholds": {},
            "alert_history": []
        })
        self.message_broker = MessageBroker()
        self.task_queue = TaskQueue()

    async def monitor_patient_vitals(self, patient_id: str, vitals_data: dict):
        """Monitor and analyze patient vital signs in real-time."""
        self.state["patient_vitals"][patient_id] = {
            "data": vitals_data,
            "timestamp": datetime.now().isoformat()
        }
        analysis = await self.analyze_vitals(patient_id, vitals_data)
        
        if analysis["alerts"]:
            await self.task_queue.submit_task({
                "type": "vital_alert",
                "patient_id": patient_id,
                "alerts": analysis["alerts"]
            }, priority=TaskPriority.HIGH)
        
        return analysis

    async def analyze_vitals(self, patient_id: str, vitals_data: dict):
        """Advanced vital signs analysis with trend detection."""
        alerts = []
        analysis = {"current": vitals_data, "trends": {}, "alerts": []}
        
        # Dynamic thresholds based on patient history
        thresholds = self.state["vital_thresholds"].get(patient_id, {
            "heart_rate": {"min": 60, "max": 100, "critical_min": 50, "critical_max": 120},
            "blood_pressure_systolic": {"min": 90, "max": 140, "critical_min": 80, "critical_max": 180},
            "blood_pressure_diastolic": {"min": 60, "max": 90, "critical_min": 50, "critical_max": 110},
            "temperature": {"min": 36.5, "max": 37.5, "critical_min": 35, "critical_max": 39},
            "oxygen_saturation": {"min": 95, "max": 100, "critical_min": 90, "critical_max": 100}
        })
        
        for vital, value in vitals_data.items():
            if vital in thresholds:
                threshold = thresholds[vital]
                if value < threshold["critical_min"] or value > threshold["critical_max"]:
                    alerts.append({
                        "level": "CRITICAL",
                        "vital": vital,
                        "value": value,
                        "message": f"Critical: {vital} severely out of range"
                    })
                elif value < threshold["min"] or value > threshold["max"]:
                    alerts.append({
                        "level": "WARNING",
                        "vital": vital,
                        "value": value,
                        "message": f"Warning: {vital} out of normal range"
                    })
                
                # Calculate trends if historical data exists
                if patient_id in self.state["patient_vitals"]:
                    history = [record[vital] for record in self.state["patient_vitals"][patient_id]]
                    if len(history) > 5:
                        trend = np.polyfit(range(len(history)), history, 1)[0]
                        analysis["trends"][vital] = {
                            "direction": "increasing" if trend > 0 else "decreasing",
                            "rate": abs(trend)
                        }
        
        if alerts:
            self.state["alert_history"].append({
                "patient_id": patient_id,
                "timestamp": datetime.now().isoformat(),
                "alerts": alerts
            })
            analysis["alerts"] = alerts
        
        return analysis

    def analyze_medical_research(self, research_data: str):
        """Analyze and summarize medical research data."""
        # Implement research data analysis using NLP
        summary = self.process_research_data(research_data)
        self.state["medical_research_data"].update(summary)
        return summary
    
    def manage_appointments(self, appointment_data: dict):
        """Manage patient appointments and scheduling."""
        self.state["appointments"].append(appointment_data)
        # Implement appointment scheduling logic
        return self.optimize_schedule()
    
    def handle_patient_records(self, patient_data: dict):
        """Manage and update patient medical records."""
        patient_id = patient_data.get("id")
        self.state["patient_records"][patient_id] = patient_data
        return {"status": "success", "message": f"Updated records for patient {patient_id}"}
    
    def analyze_vitals(self, vitals_data: dict):
        """Analyze vital signs and generate alerts if needed."""
        # Implement vital signs analysis logic
        alerts = []
        thresholds = {
            "heart_rate": {"min": 60, "max": 100},
            "blood_pressure": {"min": 90, "max": 140},
            "temperature": {"min": 36.5, "max": 37.5}
        }
        
        for vital, value in vitals_data.items():
            if vital in thresholds:
                if value < thresholds[vital]["min"] or value > thresholds[vital]["max"]:
                    alerts.append(f"Alert: {vital} out of normal range")
        
        return {"analysis": vitals_data, "alerts": alerts}
    
    def process_research_data(self, research_data: str):
        """Process and summarize medical research data."""
        # Implement research data processing logic
        # This would typically involve NLP and text summarization
        return {"summary": "Research data summary", "key_findings": []}
    
    def optimize_schedule(self):
        """Optimize appointment schedule."""
        # Implement schedule optimization logic
        return {"status": "success", "optimized_schedule": self.state["appointments"]}