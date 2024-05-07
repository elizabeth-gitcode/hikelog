from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/echo", methods=['GET'])
def echo():
    msg = request.args.get('msg')
    returned_echo = { "message": msg }    
    return jsonify(returned_echo)