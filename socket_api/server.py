import socket
import json

HOST= "127.0.0.1"
PORT = 65432

users =[]
messages=[]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"server is listening on {HOST,PORT}")
    while True:  # Keep the server running to accept multiple connections
        conn, addr = s.accept()  # Accept a new connection
        with conn:
            print(f"Connected by {addr}")
            while True:  # Loop to handle multiple requests from the same client
                data = conn.recv(1024)
                if not data:
                    break  # Break if no data is received (client closed the connection)

                request = data.decode()
                
                # request will simply return a status of the server 
                if "GET /status" in request:
                    response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "API is running"}'
                    conn.sendall(response.encode())
                # will return all messages stored within server
                elif "GET /message" in request:
                    message_dict = {"messages": messages}
                    send_this = json.dumps(message_dict)
                    response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{send_this}'
                    conn.sendall(response.encode())
                 # used to store messages in tge server should include a message in json format
                elif "POST /message" in request:
                    headers, body = request.split("\r\n\r\n", 1)
                    try:
                        format_message = json.loads(body)
                        client_message = format_message.get("message")
                        messages.append(client_message)
                        response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "Message received"}'
                        conn.sendall(response.encode())

                    except json.JSONDecodeError:
                        response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"error": "Invalid JSON format"}'
                        conn.sendall(response.encode())
                    # used to store users in the server should include a name and email 
                elif "POST /user" in request:
                    headers, body = request.split("\r\n\r\n", 1)
                    try:
                        format_message = json.loads(body)
                        client_name = format_message.get("name")
                        client_email = format_message.get("email")
                        if not client_name or not client_email:
                            missing_field = "name" if not client_name else "email"
                            response = f'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{{"error": "Missing required field: {missing_field}"}}'
                            conn.sendall(response.encode())
                        else:
                            users.append({"name": client_name, "email": client_email})
                            response = 'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{"status": "User received"}'
                            conn.sendall(response.encode())
                    except json.JSONDecodeError:
                        response = 'HTTP/1.1 400 Bad Request\nContent-Type: application/json\n\n{"error": "Invalid JSON format"}'
                        conn.sendall(response.encode())
                    # gets a user based on id should include a number at the end of request, number will match order in which users were stored
                elif "GET /user/" in request:   
                    user_id = request.split("/user/")[1].split(" ")[0]
                    user_id = int(user_id)
                    if user_id < len(users):
                        send_this = json.dumps(users[user_id])
                        response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{send_this}'
                        conn.sendall(response.encode())
                    else:
                        response = 'HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n{"error": "User not found"}'
                        conn.sendall(response.encode())
                    # returns all users
                elif "GET /user" in request:
                    send_this = json.dumps(users)
                    response = f'HTTP/1.1 200 OK\nContent-Type: application/json\n\n{send_this}'
                    conn.sendall(response.encode())

                # used if user uses a non existent endpoint
                else:
                    response = 'HTTP/1.1 404 Not Found\nContent-Type: application/json\n\n{"error": "endpoint not found"}'
                    conn.sendall(response.encode())