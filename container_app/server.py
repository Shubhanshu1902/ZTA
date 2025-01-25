from flask import Flask, jsonify
import requests
from threading import Lock
import os
import time
import json


app = Flask(__name__)
FIELDS = ["IP", "PRETTY_NAME", "NAME" , "VERSION_ID", "VERSION_CODENAME", "Image", "Platform"]
mutex = Lock()
hostname = open("/etc/hostname", "r").readline()
PORT = 5002

def deleteOutputFile(outputfile):
    try:
        print("deleting file")
        os.remove(outputfile)
    except OSError as e:
        print(e)
        
def writeToPipe(pipePath, command):
    print("writing to pipe...")
    outStream = open(pipePath, "w")
    outStream.write(command)
    outStream.close()

def readOutputFile(outputfile, isJson = False):
    data = ""
    with open(outputfile, "r") as file:
        if isJson:
            return json.load(file)[0]
        
        else:
            data = list(line + "\n" for line in (l.strip() for l in file) if line)
     
    return data

def runCommandInPipe(command, isJson = False):
    pipePath = "/hostpipe/mypipe"
    outputPath = "/hostpipe/output.txt"
    with mutex:
        deleteOutputFile(outputPath)
        writeToPipe(pipePath, command)
        time.sleep(2)
        data = readOutputFile(outputPath, isJson)
        
    return data

def getData():
    data = []
    data = runCommandInPipe("curl ifconfig.me && echo && cat /etc/os-release")
        
    dict1 = {}
    i = 0
    for line in data:
        if i == 0:
            dict1[FIELDS[i]] = line.strip("\"\n")
            i += 1
            continue
        
        command, description = line.strip().split("=")
        if i < len(FIELDS) and command == FIELDS[i]:
            dict1[FIELDS[i]] = description.strip("\"\n")
            i += 1
    
    
    data = runCommandInPipe(f"docker inspect {hostname}", True)
    
    for j in range(i, len(FIELDS)):
        dict1[FIELDS[j]] = data[FIELDS[j]]
         
    dict1["TYPE"] = "container"
    return dict1

@app.route('/getData', methods=['GET'])
def getDataRequest():
   auth_data = getData()
   print("GET DATA ")
   return jsonify({'data': auth_data})

@app.route('/make_connection', methods=['GET'])
def makeConnection():
    target_url = "http://172.16.202.130:5000/process"
    print("target url:- ", target_url)
    print("getting the data")
    headers = {"Authorization" : "Bearer my_secret_token", "Port": str(PORT)}
    
    try:
        response = requests.post(target_url, headers=headers)
        return f"Response from container 1 is : {response.json()}"
    
    except requests.exceptions.RequestException as e:
        return f"Error sending request: {e}"
    
if __name__ == "__main__":
    print("Hello world")
    app.run(host="0.0.0.0", port=PORT)
