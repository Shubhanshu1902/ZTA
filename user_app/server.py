from flask import Flask, jsonify
import socket
import requests

app = Flask(__name__)
FIELDS = ["IP", "PRETTY_NAME", "NAME" , "VERSION_ID", "VERSION_CODENAME"]
PORT=5001

def getData():
    dict1 = {}
    hostname = socket.gethostname()
    dict1["IP"] = socket.gethostbyname(hostname)
    i = 1
    
    with open('/etc/os-release') as file:
        for line in file.readlines():
            command, description = line.strip().split("=")
            if i < len(FIELDS) and command == FIELDS[i]:
                dict1[FIELDS[i]] = description.strip("\"\ \n")
                i += 1
    
    dict1["TYPE"] = "user"
    return dict1

@app.route('/getData', methods=['GET'])
def getDataRequest():
   auth_data = getData()
   print("auth data :- ", auth_data)
   return jsonify({'data': auth_data})

@app.route('/make_connection', methods=['GET'])
def makeConnection():
    target_url = "http://172.16.202.130:5000/process"
    auth_data = getData()
    headers = {"Authorization" : "Bearer my_secret_token", "Port": str(PORT)}
    
    try:
        response = requests.post(target_url, headers=headers)
        return f"Response from container 1 is : {response.json()}"
    
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
