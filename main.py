"""TODO:
    - functions to update database with callback data
    - functions to send emails to self and guest for successful payment
"""
from flask import Flask, request
import json
import os
from revolut import process_revolut_callback, verify_revolut_payload_signature


app = Flask(__name__)


@app.route("/revolutcallback", methods=["POST"])
def revolutcallback():
    headers = request.headers
    raw_data = request.data
    
    isRevolut = verify_revolut_payload_signature(headers, raw_data)
    if not isRevolut:
        return "Invalid Revolut callback received!", 400
    
    data = json.loads(raw_data)  # Attempt to parse the incoming data as JSON

    if not data['event'] in ('ORDER_COMPLETED', 'ORDER_CANCELLED'):
        return 200
    
    process_revolut_callback(data)
    return 200


@app.route("/test", methods=["POST"])
def hook():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    from correspondence.self.functions import new_email_to_self, send_email_to_self
    user, message = new_email_to_self(subject = "Local contact received")
    message.body.paragraph(f"Received data: {data}")
    send_email_to_self(user, message)
    return "Hello, world!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)