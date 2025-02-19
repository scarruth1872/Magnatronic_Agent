from flask import jsonify
from functools import wraps
import time

def json_response(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if isinstance(result, tuple):
                response = jsonify(result[0]), result[1]
            else:
                response = jsonify(result)
            if isinstance(response, tuple):
                response[0].headers['Content-Type'] = 'application/json'
            else:
                response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            error_response = {
                'error': str(e),
                'timestamp': time.time()
            }
            return jsonify(error_response), 500
    return decorated_function

@json_response
def get_nlp_metrics():
    # Mock metrics for now - replace with actual metrics from NLP agent
    return {
        'requestCount': 100,
        'errorCount': 5,
        'avgProcessingTime': 0.5
    }

@json_response
def process_nlp_request(data):
    try:
        action = data.get('action')
        text = data.get('text')
        target_language = data.get('targetLanguage')
        
        # Mock processing based on action
        if action == 'translate':
            result = f"Translated text to {target_language}"
        elif action == 'analyze':
            result = "Analysis results for the text"
        elif action == 'summarize':
            result = "Summary of the text"
        else:
            return jsonify({'error': 'Invalid action'}), 400
            
        return {
            'result': result,
            'status': 'success',
            'timestamp': time.time()
        }
    except Exception as e:
        return {'error': str(e)}, 500