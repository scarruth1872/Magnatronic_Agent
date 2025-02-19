from flask import Blueprint, request
from .api_handlers import get_nlp_metrics, process_nlp_request

api = Blueprint('api', __name__)

@api.route('/api/nlp/metrics')
def nlp_metrics():
    response = get_nlp_metrics()
    return response

@api.route('/api/nlp', methods=['POST'])
def nlp_process():
    data = request.get_json()
    return process_nlp_request(data)