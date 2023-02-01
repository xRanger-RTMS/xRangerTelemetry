# xRangerTelemetry

The telemetry backend of the xRanger RTMS.

## Deployment
- Create a python virtual environment with command `python3 -m venv venv`
- Activate the virtual environment (Windows: `source .\venv\Scripts\activate`)
- Install dependencies `pip install -r requirements.txt`
- Start the server by typing `python3 main.py` in the terminal.
- Go to `http://127.0.0.1:15000/api/v1/realtime/status` in the browser. If it shows `{"status":"online"}` then the server is running.

