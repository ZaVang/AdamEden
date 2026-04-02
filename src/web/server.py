from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    try:
        with open('/app/data/Diary.md', 'r', encoding='utf-8') as f:
            content = f.read()
        # 使用三引号避免单撇号 ('s) 导致的语法错误
        return f"""<html><body><h1>Adam's Evolution</h1><pre>{content}</pre></body></html>"""
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

def run_server():
    # 保持在 8080 端口，与圣经一致
    app.run(host='0.0.0.0', port=8080)