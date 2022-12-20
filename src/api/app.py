from flask import Flask
from flask_cors import CORS

from api.realtime.app_realtime import realtime_api
from config import API_LISTEN_IP, API_LISTEN_PORT

app = Flask(__name__)
CORS(app)

# register blueprint with url prefix '/api/v1'
app.register_blueprint(realtime_api, url_prefix='/api/v1/realtime')

@app.errorhandler(Exception)
def handle_exception(e):
    return {
               "code": getattr(e, "code", 500),
               "message": str(e)
           }, getattr(e, "code", 500)

@app.route("/status")
def status():
    return {
        "message": "OK"
    }


if __name__ == "__main__":
    app.run(host=API_LISTEN_IP, port=API_LISTEN_PORT)