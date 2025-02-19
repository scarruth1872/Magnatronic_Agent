from typing import Dict, List, Optional
from ..core.agent import Agent
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqTransummarization
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import nltk

class NLPAgent(Agent):
    """Natural Language Processing Agent for handling various NLP tasks."""

    def __init__(self):
        super().__init__()
        self.translation_model = None
        self.summarizer = None
        self.ner_model = None
        self.conversation_model = None
        self.message_broker = MessageBroker()
        self.performance_metrics = {
            'request_count': 0,
            'error_count': 0,
            'processing_times': []
        }
        self._initialize_models()
        self._start_performance_monitoring()

    def _initialize_models(self):
        """Initialize NLP models and download required NLTK data."""
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

        # Initialize translation pipeline
        self.translation_model = pipeline('translation', model='Helsinki-NLP/opus-mt-en-ROMANCE')
        
        # Initialize summarization pipeline
        self.summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
        
        # Initialize NER pipeline
        self.ner_model = pipeline('ner', model='dbmdz/bert-large-cased-finetuned-conll03-english')

    def _start_performance_monitoring(self):
        """Initialize performance monitoring for this agent."""
        self.performance_metrics = {
            'request_count': 0,
            'error_count': 0,
            'processing_times': [],
            'last_update': time.time()
        }

    async def _update_metrics(self, processing_time: float, error: bool = False):
        """Update performance metrics and send to monitoring agent."""
        self.performance_metrics['request_count'] += 1
        if error:
            self.performance_metrics['error_count'] += 1
        self.performance_metrics['processing_times'].append(processing_time)
        
        # Keep only last 100 processing times
        if len(self.performance_metrics['processing_times']) > 100:
            self.performance_metrics['processing_times'].pop(0)
        
        # Calculate average processing time
        avg_time = sum(self.performance_metrics['processing_times']) / len(self.performance_metrics['processing_times'])
        
        # Send metrics to monitoring agent
        await self.message_broker.send_message(
            sender_id=self.id,
            recipient_id='monitoring_agent',
            message={
                'type': 'performance_update',
                'metrics': {
                    'request_count': self.performance_metrics['request_count'],
                    'error_count': self.performance_metrics['error_count'],
                    'avg_processing_time': avg_time,
                    'timestamp': time.time()
                }
            }
        )

    async def translate_text(self, text: str, target_lang: str) -> str:
        """Translate text to target language."""
        start_time = time.time()
        try:
            translation = self.translation_model(text, target_lang=target_lang)
            result = translation[0]['translation_text']
            await self._update_metrics(time.time() - start_time)
            return result
        except Exception as e:
            self.logger.error(f"Translation error: {str(e)}")
            await self._update_metrics(time.time() - start_time, error=True)
            return ""

    def analyze_text(self, text: str) -> Dict:
        """Perform text analysis including entity recognition and summarization."""
        try:
            # Named Entity Recognition
            entities = self.ner_model(text)
            
            # Text summarization
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            
            return {
                'entities': entities,
                'summary': summary[0]['summary_text']
            }
        except Exception as e:
            self.logger.error(f"Text analysis error: {str(e)}")
            return {'entities': [], 'summary': ''}

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract named entities from text using NLTK."""
        try:
            # Tokenize and tag the text
            tokens = word_tokenize(text)
            tagged = pos_tag(tokens)
            entities = ne_chunk(tagged)
            
            # Extract named entities
            named_entities = []
            for chunk in entities:
                if hasattr(chunk, 'label'):
                    named_entities.append({
                        'text': ' '.join(c[0] for c in chunk),
                        'type': chunk.label()
                    })
            return named_entities
        except Exception as e:
            self.logger.error(f"Entity extraction error: {str(e)}")
            return []

    def process_conversation(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Process conversational input and generate appropriate response."""
        try:
            # Initialize conversation pipeline if not already done
            if self.conversation_model is None:
                self.conversation_model = pipeline('conversational', 
                                                 model='microsoft/DialoGPT-medium')
            
            # Generate response based on user input and context
            response = self.conversation_model(user_input, context=context)
            return response[0]['generated_text']
        except Exception as e:
            self.logger.error(f"Conversation processing error: {str(e)}")
            return ""