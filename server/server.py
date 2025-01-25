from flask import Flask, request, jsonify
import requests as req
import json

app = Flask(__name__)
hostname = open("/etc/hostname", "r").readline()

connections = []
SECRET_TOKEN = "my_secret_token"
USER  = "user"
CONTAINER = "container"

def getJSONPolicy(actor_type):
    filename = ""
    if actor_type == USER:
        filename = "user_policy.json"
        
    elif actor_type == CONTAINER:
        filename = "container_policy.json"
        
    else:
        return {}
    
    with open(filename) as file:
        data = json.load(file)
        
    return data

def getFields(actor_type):
    if actor_type == USER:
        return ["IP", "PRETTY_NAME", "NAME" , "VERSION_ID", "VERSION_CODENAME"]
    
    elif actor_type == CONTAINER:
        return ["IP", "PRETTY_NAME", "NAME" , "VERSION_ID", "VERSION_CODENAME", "Image", "Platform"]
    
    else:
        return []

def verifyData(data, actor_type):
    policy = getJSONPolicy(actor_type)
    fields = getFields(actor_type)
    if len(policy) != len(fields):
        return False
    
    covered = 0
    for k in policy:
        if k in fields:
            covered += 1
            if (k not in data) or (data[k] not in policy[k]):
                return False
             
    if covered == len(fields):
        return True
    
    return False

@app.before_request
def authenticate_request():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {SECRET_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401
    
    port = request.headers.get("Port")
    print(port)
    target_ip = f"http://{request.remote_addr}:{port}/getData"
    print(target_ip)
    resp = req.get(target_ip)
    data = resp.json()['data']
    print(data)
    if not (data and "TYPE" in data and data['TYPE'] in [USER, CONTAINER]):
        return jsonify({"error": "no type", "data" : data}), 401
    
    actor_type = data["TYPE"]
    ack = verifyData(actor_type, data)
    if not ack:
        return jsonify({"error": "Unauthorized", "dict" : data}), 401
    

@app.route('/process', methods=['POST'])
def process_request():
    # Process the authenticated request
    data = request.get_json()
    return jsonify({"message": "Request processed successfully", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
