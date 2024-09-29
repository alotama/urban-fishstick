from flask import jsonify

def handle_response(data, status):
    response = jsonify(data)
    response.status_code = status
    return response