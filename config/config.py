import json

def load_config():
    try:
        with open('./config/config.json') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Error: config.json no encontrado.")
        exit(1)

def load_request_schema():
    try:
        with open('./config/request_schema.json') as schema_file:
            return json.load(schema_file)
    except FileNotFoundError:
        print("Error: request_schema.json no encontrado.")
        exit(1)