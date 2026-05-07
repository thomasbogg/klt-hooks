from flask import Flask, request
from settings import LOCAL, SECRET_KEY
import json
import os

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def hook():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    print(f"Received data: {data}")
    return "Hello, world!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)