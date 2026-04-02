from src.web.server import app

def run_server():
    app.run(host="0.0.0.0", port=8080)
