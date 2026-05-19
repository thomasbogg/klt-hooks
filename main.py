from flask import Flask, request
import json
import os
from revolut import process_revolut_callback, verify_revolut_payload_signature


app = Flask(__name__)


@app.route("/revolut/callback", methods=["POST"])
def revolutcallback():
    try:
        if not verify_revolut_payload_signature(request.headers, request.data):
            return ('', 204) # Return 204 to indicate that the callback was received

        data = json.loads(request.data)  
        if not data['event'] == 'ORDER_COMPLETED':
            _contact_self_for_error(f"Received unexpected event type: {data['event']}", request.data.decode('utf-8'), dict(request.headers))
            return ('', 204) # Return 204 to indicate that the callback was received, even if it's not the event we're interested in

        process_revolut_callback(data)
  
    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))
  
    return ('', 204) # Return 204 to indicate that the callback was received, even if there was an error processing it

"""
@app.route("/wise/callback", methods=["POST"])
def wisecallback():
    try:
        headers = request.headers
        data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
        
        from correspondence.self.functions import new_email_to_self, send_email_to_self
        user, message = new_email_to_self(subject = "Wise callback received")
        message.body.paragraph("Headers:")
        for key, value in headers.items():
            message.body.paragraph(f"{key}: {value}")
        message.body.paragraph(f"Received data: {data}")
        send_email_to_self(user, message)
 
    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))
 
    return ('', 200) # Return 200 to indicate that the callback was received

"""
@app.route("/test", methods=["POST"])
def hook():
    data = json.loads(request.data)  # Attempt to parse the incoming data as JSON
    from correspondence.self.functions import new_email_to_self, send_email_to_self
    user, message = new_email_to_self(subject = "Local contact received")
    message.body.paragraph(f"Received data: {data}")
    send_email_to_self(user, message)
    return "Hello, world!"


def _contact_self_for_error(e: str, data: str, headers: dict) -> None:
    from correspondence.self.functions import new_email_to_self, send_email_to_self
    user, message = new_email_to_self(subject = f"Error occurred: {e}")
    message.body.paragraph(f"Error: {e}")
    message.body.paragraph(f"Data: {data}")
    message.body.paragraph(f"Headers: {headers}")
    send_email_to_self(user, message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)