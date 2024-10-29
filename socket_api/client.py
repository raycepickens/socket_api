import socket
import json  # Import to handle JSON conversion

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        response = s.recv(1024)
    return response.decode()

def test_status():
    request = "GET /status HTTP/1.1\r\n"
    request += f"Host: {HOST}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    response = send_request(request)
    print(f"Status Response:\n{response}")

def test_post_message():
    body = json.dumps({"message": "Hello, world!"})  # Convert dictionary to JSON string
    content_length = len(body)
    request = "POST /message HTTP/1.1\r\n"  # The request line
    request += f"Host: {HOST}\r\n"  # Host header
    request += "Content-Type: application/json\r\n"  # Content-Type header
    request += f"Content-Length: {content_length}\r\n"  # Content-Length header
    request += "Connection: close\r\n"  # Connection header
    request += "\r\n"  # End of headers
    request += body  # Add the JSON body
    response = send_request(request)
    print(f"Post Message Response:\n{response}")

def test_post_user(name, email):
    body = json.dumps({"name": name, "email": email})  # Convert dictionary to JSON string
    content_length = len(body)
    request = "POST /user HTTP/1.1\r\n"
    request += f"Host: {HOST}\r\n"
    request += "Content-Type: application/json\r\n"
    request += f"Content-Length: {content_length}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    request += body
    response = send_request(request)
    print(f"Post User Response:\n{response}")

def test_get_users():
    request = "GET /user HTTP/1.1\r\n"
    request += f"Host: {HOST}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    response = send_request(request)
    print(f"Get Users Response:\n{response}")

def test_get_user_by_id(user_id):
    request = f"GET /user/{user_id} HTTP/1.1\r\n"
    request += f"Host: {HOST}\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    response = send_request(request)
    print(f"Get User by ID Response:\n{response}")

if __name__ == "__main__":
    test_status()  # Test /status endpoint
    test_post_message()  # Test /message endpoint

    # Test adding users
    test_post_user("Alice", "alice@example.com")
    test_post_user("Bob", "bob@example.com")

    # Test getting all users
    test_get_users()  # Test /user endpoint

    # Test getting users by ID
    test_get_user_by_id(0)  # Test /user/0
    test_get_user_by_id(1)  # Test /user/1
    test_get_user_by_id(999)  # Test a non-existent user ID for error response
