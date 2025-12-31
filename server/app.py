from flask import Flask
from flask_cors import CORS

from schema import schema
from routes import register_routes
from conf import get_config
from container import Container

def create_app():
    app = Flask(__name__)
    config = get_config()
    Container.init(config)
    CORS(app)
    register_routes(app, schema)
    return app
    
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
