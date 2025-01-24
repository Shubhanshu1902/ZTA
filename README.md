Requirements:
1. Docker
2. Python with flask

Instructions to run the code.
1. Run: ```mk fifo pipe/{pipeName}```
2. while true; ```do eval "$(cat pipe/{pipeName})" > pipe/ output.txt; done```
3. Run the docker compose file: ```docker compose up```
4. Server container runs on port 5000 and client container runs on port 5002
5. If you want to run this as a user, run the file ```user_app/server.py```. This will start a flask app.
6. If you want to send a request to the server via the client container, on a web browser, run(if running locally, change IP if running on a VM) ```localhost:5002/make_connection```
7. Change the policy according to your use case or testing.
