from magnatronic.core.agent import Agent
from transformers import pipeline
from typing import Dict, Any
import numpy as np

class SentimentAnalysisAgent(Agent):
    def __init__(self):
        super().__init__("sentiment_analysis")
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

    async def detect_emotion(self, text: str) -> Dict[str, float]:
        """Detect emotions in the given text."""
        results = self.emotion_classifier(text)[0]
        return {item['label']: item['score'] for item in results}

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the sentiment of the given text."""
        result = self.sentiment_analyzer(text)[0]
        return {
            'sentiment': result['label'],
            'confidence': result['score']
        }

    async def generate_emotional_response(self, text: str, base_response: str) -> str:
        """Generate an emotionally appropriate response based on detected sentiment."""
        sentiment = await self.analyze_sentiment(text)
        emotions = await self.detect_emotion(text)
        
        # Adjust response based on detected emotions
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        response_modifiers = {
            'joy': 'enthusiastically',
            'sadness': 'empathetically',
            'anger': 'calmly',
            'fear': 'reassuringly',
            'surprise': 'attentively',
            'love': 'warmly'
        }
        
        modifier = response_modifiers.get(dominant_emotion, '')
        if modifier:
            base_response = f"{modifier.capitalize()}, {base_response.lower()}"
        
        return base_response

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming tasks based on their type."""
        task_type = task_data.get('type')
        text = task_data.get('text', '')
        
        if task_type == 'emotion_detection':
            return await self.detect_emotion(text)
        elif task_type == 'sentiment_analysis':
            return await self.analyze_sentiment(text)
        elif task_type == 'emotional_response':
            base_response = task_data.get('base_response', '')
            return {'response': await self.generate_emotional_response(text, base_response)}
        else:
            raise ValueError(f"Unknown task type: {task_type}")