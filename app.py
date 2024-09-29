from flask import Flask, request
import json
from jsonschema import validate, ValidationError

from services.compare_names import compare_names
from utils.load_names import load_names
from utils.handle_response import handle_response
from services.cache_service import cache

app = Flask(__name__)

try:
    with open('./config.json') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Error: config.json no encontrado.")
    exit(1)

try:
    with open('./request_schema.json') as schema_file:
        request_schema = json.load(schema_file)
except FileNotFoundError:
    print("Error: request_schema.json no encontrado.")
    exit(1)

@app.route('/areCompromisedNames', methods=['POST'])
def compare():
    try:
        data = request.get_json()
        
        # Validate the request body
        validate(instance=data, schema=request_schema)
        
        input_names = data['names']
        similarity_threshold = config['similarity_threshold']
        
        name_list = load_names('assets/names_dataset.csv')
        
        results = []
        for input_name in input_names:
            cache_key = (input_name, similarity_threshold)
            if cache_key in cache:
                print(f"Result for {input_name} obtained from cache")
                compromised_name = cache[cache_key]
            else:
                comparison_results = compare_names(input_name, name_list, similarity_threshold)
                compromised_name = len(comparison_results) > 0
                cache[cache_key] = compromised_name
            
            results.append({
                'name': input_name,
                'compromised_name': compromised_name
            })
        
        return handle_response(results, status=200)
    except ValidationError as e:
        return handle_response({'error': f'Invalid request: {e.message}'}, status=400)
    except Exception as e:
        return handle_response({'error': str(e)}, status=500)

if __name__ == '__main__':
    app.run(debug=True)