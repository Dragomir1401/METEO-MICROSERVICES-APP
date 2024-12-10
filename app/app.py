from flask import Flask
from endpoints.countries import cntrs_bp
from endpoints.cities import ct_bp
from endpoints.temperatures import tmp_bp

app = Flask(__name__)

# Blueprint registration
app.register_blueprint(cntrs_bp)
app.register_blueprint(ct_bp)
app.register_blueprint(tmp_bp)

if __name__ == '__main__':
    # Debug mode is for automatic reloading
    app.run(host='0.0.0.0', port=5000, debug=True)
