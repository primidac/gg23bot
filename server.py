from flask import Flask
import threading
from bot import main

app = Flask(__name__)

@app.route("/")
def home():
    return "B<>rder/ess GG23 Bot is running!"

threading.Thread(target=main).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)