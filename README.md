# Simple Python HTTP Server with User and Message Storage

This is a simple HTTP server built using Python's `socket` library to handle HTTP requests. The server listens on a specified IP and port and provides endpoints to store and retrieve user and message data.

## Features

- **GET /status** - Check the status of the server.
- **GET /message** - Retrieve all messages stored on the server.
- **POST /message** - Send a message to be stored on the server (expects JSON format).
- **POST /user** - Add a user with a name and email (expects JSON format).
- **GET /user/[id]** - Retrieve user information based on the user's stored order.
- **GET /user** - Retrieve all stored users.
- **Error Handling** - Handles invalid JSON and missing fields for POST requests, as well as non-existent endpoints.

## Requirements

- Python 3.x

## Usage

1. **Start the Server**

   To start the server, run the Python script:
   ```bash
   python server.py



notes:
server does not have a working data-base and currently uses variables to store data, so any info stored will only be saved in the session it was created in
client is bare bones and was used for testing along the way, should not be used as a comprehensive test tool
