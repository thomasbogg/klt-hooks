from flask import Flask, request


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def hook():
    print(request.data)
    return "Hello, world!"