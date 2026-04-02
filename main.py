import threading
from src.web.server import run_server
import time

if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print('Adam is alive and the web server is running on port 8081.')
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass