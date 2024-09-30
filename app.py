from flask import Flask, request
import json
from jsonschema import validate, ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from services.compare_names import compare_names
from utils.load_names import load_names
from utils.handle_response import handle_response
from services.cache_service import cache
from utils.encryption import decrypt_file, encrypt_file, generate_key

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

try:
    env_encryption_key = config['env_encryption_key'].encode()
except KeyError:
    print("Error: env_encryption_key no encontrado en config.json.")
    exit(1)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[config.get("default_limits", "60 per minute")]
)

@app.route('/areCompromisedNames', methods=['POST'])
def compare():
    try:
        data = request.get_json()
        
        validate(instance=data, schema=request_schema)
        
        input_names = data['names']
        similarity_threshold = config['similarity_threshold']
        

        decrypt_file('assets/names_dataset.csv', env_encryption_key)
        name_list = load_names('assets/names_dataset.csv')
        encrypt_file('assets/names_dataset.csv', env_encryption_key)
        
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