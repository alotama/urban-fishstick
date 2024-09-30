from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from jsonschema import validate, ValidationError
from services.cache_service import cache
from services.compare_names import compare_names
from utils.load_names import load_names
from utils.handle_response import handle_response
from utils.encryption import decrypt_file, encrypt_file
from config.config import load_config, load_request_schema

main_bp = Blueprint('main', __name__)

config = load_config()
request_schema = load_request_schema()

try:
    env_encryption_key = config['env_encryption_key'].encode()
except KeyError as e:
    print(f"Error: {e} no encontrado en config.json.")
    exit(1)

@main_bp.route('/areCompromisedNames', methods=['POST'])
@jwt_required()
def compare():
    try:
        data = request.get_json()
        
        validate(instance=data, schema=request_schema)
        
        input_names = data['names']
        similarity_threshold = data['similarity_threshold']
        
        decrypt_file('assets/names_dataset.csv', env_encryption_key)
        name_list = load_names('assets/names_dataset.csv')
        encrypt_file('assets/names_dataset.csv', env_encryption_key)
        
        results = {}
        for input_name in input_names:
            cache_key = (input_name, similarity_threshold)
            if cache_key in cache:
                print(f"Result for {input_name} obtained from cache")
                comparison_results = cache[cache_key]
            else:
                comparison_results = compare_names(input_name, name_list, similarity_threshold)
                cache[cache_key] = comparison_results
            
            if comparison_results:
                results[input_name] = comparison_results
        
        sorted_results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1][0]['similarity'], reverse=True) if v}
        
        return handle_response(sorted_results, status=200)
    except ValidationError as e:
        return handle_response({'error': f'Invalid request: {e.message}'}, status=400)
    except IndexError as e:
        return handle_response({'error': 'list index out of range'}, status=500)
    except Exception as e:
        return handle_response({'error': str(e)}, status=500)