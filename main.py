from flask import Flask, request
import json
import os
from revolut import process_revolut_merchant_callback, verify_revolut_payload_signature
from default.settings import REVOLUT_MERCHANT_API_SIGNING_KEY


app = Flask(__name__)


@app.route("/revolut/callback", methods=["POST"])
def revolut_merchant_callback():
    try:
        if verify_revolut_payload_signature(request.headers, request.data, REVOLUT_MERCHANT_API_SIGNING_KEY):

            data = json.loads(request.data)  
            if not data['event'] == 'ORDER_COMPLETED':
                _contact_self_for_error(f"Received unexpected event type: {data['event']}", request.data.decode('utf-8'), dict(request.headers))
            else:
                process_revolut_merchant_callback(data)
  
    except Exception as e:
        _contact_self_for_error(str(e), request.data.decode('utf-8'), dict(request.headers))
  
    return ('', 204) # Return 204 to indicate that the callback was received, even if there was an error processing it


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