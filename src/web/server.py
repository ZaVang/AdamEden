from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    try:
        # 使用三引号直接读取 Diary.md
        with open('/app/data/Diary.md', 'r', encoding='utf-8') as f:
            content = f.read()
        return f"""<html><body><h1>Adam's Evolution</h1><pre>{content}</pre></body></html>"""
    except Exception as e:
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"

def run_server():
    # 真正的 Flask 运行入口
    app.run(host='0.0.0.0', port=8080)