from socket import *
import json
import sqlite3
import hashlib
import numpy as np
from Levenshtein import distance


# Levenshtein to Give hints according to the similarity between the input name and the names in db
def hint_name(input_name, name_list):
    distances = np.array(
        [distance(input_name.lower(), name.lower()) for name in name_list]
    )
    closest_index = np.argmin(distances)
    return name_list[closest_index]


# Set the Allowed Host for the CORS permissions
allowedHost = "http://localhost:8000"

# Creating a Database
conn = sqlite3.connect("restData.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")

# Creating a table of useres and passwords then Check if the result is not None
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")

name_list = ["basheer", "ahmad", "essa", "admin", "Sami", "ali"]
pass_list = ["basheer", "ahmad", "essa", "admin", "Sami", "ali"]

for i in range(len(name_list)):
    username = name_list[i]
    password = pass_list[i]
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{hashed_password}')")
    conn.commit()

# Starting a server which listens to 5 concurrent users
serverPort = 4000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("RestAPI is Ready")


def authenticate(username, password):
    entered_password = hashlib.sha256(password.encode()).hexdigest()
    # Searching in the databse for the specefic user to give authentication
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}';")
    # if there exists a user with the given credintels then give him the permission or not
    result = cursor.fetchone()
    if result is None:
        """There is no user with the username given"""
        return "nouser"
    if result:

        hashed_password = result[1]
        # print("Entered: ", entered_password)
        # print("Hashed: ", hashed_password)
        if entered_password == hashed_password:
            return "true"
    return "false"


while True:
    connectionSocket, clientAddress = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    ip = clientAddress[0]
    port = clientAddress[1]
    list = sentence.split(" ")
    method = list[0]
    print(method)

    if list[1] == "/login":
        if method == "GET":
            response = {
                "message": "Hello You made a Get request",
                "Information": "Please Provide in a new message your name and password to proceed authentication.",
            }
            response_json = json.dumps(response)

            connectionSocket.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))
            connectionSocket.send("Content-Type: application/json\r\n".encode("utf-8"))
            connectionSocket.send(
                (f"Access-Control-Allow-Origin: {allowedHost}\r\n").encode("utf-8")
            )
            connectionSocket.send(
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n".encode("utf-8")
            )
            connectionSocket.send(
                "Access-Control-Allow-Headers: Content-Type\r\n".encode("utf-8")
            )
            connectionSocket.send("\r\n".encode("utf-8"))
            connectionSocket.send(response_json.encode("utf-8"))
            connectionSocket.close()

        elif method == "POST":
            data = sentence
            start = data.find("{")
            end = data.rfind("}") + 1
            json_data = data[start:end]
            # Transform recieved data from JSON to Python
            object_data = json.loads(json_data)
            print(object_data)
            username = object_data["name"]
            password = object_data["password"]
            isAuthenticated = authenticate(username, password)
            if isAuthenticated == "true":
                response = {
                    "message": f"Hello {username}",
                    "Authenticated": "You can use the system.",
                }
                response_json = json.dumps(response)
                connectionSocket.send("HTTP/1.0 200 OK\r\n".encode("utf-8"))

            elif isAuthenticated == "false":
                response = {
                    "message": f"Sorry but {username} Failed to be authenticated.",
                    "Not Authenticated": "You can try again.",
                }
                response_json = json.dumps(response)
                connectionSocket.send("HTTP/1.1 401 Unauthorized\r\n".encode("utf-8"))
            elif isAuthenticated == "nouser":
                response = {
                    "message": f"Sorry but can't find user: {username}.",
                    "hint": f"Do you mean {hint_name(username, name_list)} ?",
                }
                response_json = json.dumps(response)
                connectionSocket.send("HTTP/1.1 401 Unauthorized\r\n".encode("utf-8"))

            connectionSocket.send("Content-Type: application/json\r\n".encode("utf-8"))
            connectionSocket.send(
                (f"Access-Control-Allow-Origin: {allowedHost}\r\n").encode("utf-8")
            )
            connectionSocket.send(
                "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n".encode("utf-8")
            )
            connectionSocket.send(
                "Access-Control-Allow-Headers: Content-Type\r\n".encode("utf-8")
            )
            connectionSocket.send("\r\n".encode("utf-8"))
            connectionSocket.send(response_json.encode("utf-8"))
            connectionSocket.close()
