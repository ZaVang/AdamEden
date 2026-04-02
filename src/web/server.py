from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('/app/data/Diary.md', 'r', encoding='utf-8') as f:
            content = f.read()
        return f'<html><body><h1>Adam's Evolution</h1><pre>{content}</pre></body></html>'
    except Exception as e:
        return f'Error reading diary: {e}'

def run_server():
    app.run(host='0.0.0.0', port=8081)