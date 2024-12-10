from flask import Flask
import socket
import requests

app = Flask(__name__)
FIELDS = ["IP", "PRETTY_NAME", "NAME" , "VERSION_ID", "VERSION_CODENAME"]

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

@app.route('/make_connection', methods=['GET'])
def makeConnection():
    target_url = "http://172.16.202.126:5000/process"
    auth_data = getData()
    headers = {"Authorization" : "Bearer my_secret_token"}
    
    try:
        response = requests.post(target_url, json=auth_data, headers=headers)
        return f"Response from container 1 is : {response.json()}"
    
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)