from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.config import load_config, load_request_schema
from routes.login import auth_bp
from routes.areCompromisedNames import main_bp

app = Flask(__name__)

config = load_config()
request_schema = load_request_schema()

try:
    env_encryption_key = config['env_encryption_key'].encode()
    jwt_secret_key = config['env_JWT_SECRET_KEY']
except KeyError as e:
    print(f"Error: {e} no encontrado en config.json.")
    exit(1)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[config.get("default_limits", "60 per minute")]
)

app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)