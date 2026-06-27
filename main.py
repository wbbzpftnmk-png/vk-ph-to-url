import threading
import webview
from app import app

HOST = "127.0.0.1"
PORT = 5000
URL = f"http://{HOST}:{PORT}"

def run_server():
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    webview.create_window(
        title="VK Album Photo URLs",
        url=URL,
        width=1100,
        height=800,
        resizable=True,
        confirm_close=True
    )
    webview.start()
