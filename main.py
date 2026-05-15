
from correspondence.self.functions import new_email_to_self, send_email_to_self
from flask import Flask, Request, request
import json
import os
from werkzeug.datastructures import Headers
from revolut import process_revolut_callback
from wrapper import update

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
    headers = request.headers
    raw_data = request.data
    
    isRevolut = verify_revolut_payload_signature(headers, raw_data)
    if not isRevolut:
        user, message = new_email_to_self(subject = "Invalid Revolut contact received")
        message.body.paragraph(f"Received headers: {headers}")
        message.body.paragraph(f"Received data: {raw_data}")
        send_email_to_self(user, message)
        return "Invalid Revolut contact received!", 400
    
    data = json.loads(raw_data)  # Attempt to parse the incoming data as JSON

    if not data['event'] == 'ORDER_COMPLETED':
        return 400
    
    process_revolut_callback(data)
    return 400


def verify_revolut_payload_signature(headers: Headers, raw_data: bytes) -> bool:
    import hmac
    import hashlib
    signing_secret = os.getenv('REVOLUT_API_SIGNING_KEY')
    timestamp = headers.get('Revolut-Request-Timestamp')
    payload_to_sign = 'v1.' + timestamp + '.' + raw_data.decode('utf-8')
    signature = 'v1=' + hmac.new(bytes(signing_secret, 'utf-8'), msg = bytes(payload_to_sign, 'utf-8'), digestmod = hashlib.sha256).hexdigest()
    is_revolut = signature == headers.get('Revolut-Signature')
    return signing_secret, timestamp, payload_to_sign, signature, is_revolut


if __name__ == "__main__":
    user, message = new_email_to_self(subject = "KLT Hooks starting")
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)