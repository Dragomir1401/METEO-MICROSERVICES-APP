from flask import Flask
from endpoints.countries import cntrs_bp
from endpoints.cities import ct_bp
from endpoints.temperatures import tmp_bp

app = Flask(__name__)

# Register the blueprints for each table
app.register_blueprint(cntrs_bp)
app.register_blueprint(ct_bp)
app.register_blueprint(tmp_bp)

if __name__ == '__main__':
    # Run the app with debug mode enabled to auto-reload on changes
    app.run(host='0.0.0.0', port=5000, debug=True)
