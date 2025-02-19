from magnatronic.core.agent import Agent
from typing import Dict, Any
import speech_recognition as sr
import pyttsx3

class VoiceInteractionAgent(Agent):
    def __init__(self):
        super().__init__("voice_interaction")
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()

    async def recognize_speech(self) -> Dict[str, Any]:
        """Convert speech to text using microphone input."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return {
                    'success': True,
                    'text': text
                }
        except sr.UnknownValueError:
            return {
                'success': False,
                'error': 'Speech could not be understood'
            }
        except sr.RequestError as e:
            return {
                'success': False,
                'error': f'Could not request results; {str(e)}'
            }

    async def process_voice_command(self, command: str) -> Dict[str, Any]:
        """Process voice commands and determine appropriate actions."""
        command = command.lower()
        
        # Basic command processing logic
        if 'search' in command:
            return {
                'action': 'search',
                'query': command.replace('search', '').strip()
            }
        elif 'analyze' in command:
            return {
                'action': 'analyze',
                'content': command.replace('analyze', '').strip()
            }
        else:
            return {
                'action': 'unknown',
                'command': command
            }

    async def generate_voice_feedback(self, text: str) -> None:
        """Convert text to speech and play it."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming tasks based on their type."""
        task_type = task_data.get('type')
        
        if task_type == 'speech_recognition':
            return await self.recognize_speech()
        elif task_type == 'voice_command':
            command = task_data.get('command', '')
            return await self.process_voice_command(command)
        elif task_type == 'voice_feedback':
            text = task_data.get('text', '')
            await self.generate_voice_feedback(text)
            return {'success': True}
        else:
            raise ValueError(f"Unknown task type: {task_type}")