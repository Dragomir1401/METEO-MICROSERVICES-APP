from flask import Flask
from endpoints.countries import countries_bp
from endpoints.cities import cities_bp
from endpoints.temperatures import temperatures_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(countries_bp)
app.register_blueprint(cities_bp)
app.register_blueprint(temperatures_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
