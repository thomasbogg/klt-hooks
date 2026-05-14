from correspondence.self.functions import new_email_to_self, send_email_to_self
from flask import Flask, request
import json
import os

app = Flask(__name__)

@app.route("/test", methods=["POST"])
def hook():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    user, message = new_email_to_self(subject = "Local contact received")
    message.body.paragraph(f"Received data: {data}")
    send_email_to_self(user, message)
    return "Hello, world!"


@app.route("/wisecallback", methods=["POST"])
def wisecallback():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    print(f"Received data: {data}")
    return "Wise Money In contact received!"


@app.route("/revolutcallback", methods=["POST"])
def revolutcallback():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    headers = json.loads(request.headers)
    if data['event'] == 'ORDER_AUTHORISED':
        user, message = new_email_to_self(subject = "Revolut order authorised")
    # 'event': 'ORDER_AUTHORISED', 'order_id': '6a05fb0c-d53e-a0fb-b8f5-854b9a51bc33'
    elif data['event'] == 'ORDER_COMPLETED':
        user, message = new_email_to_self(subject = "Revolut order completed")
    message.body.paragraph(f"Received headers: {headers}")
    message.body.paragraph(f"Received data: {data}")
    send_email_to_self(user, message)
    return "Revolut contact received!"


if __name__ == "__main__":
    user, message = new_email_to_self(subject = "KLT Hooks starting")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)