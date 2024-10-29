from fastapi import FastAPI, WebSocket
from paramiko import SSHClient, AutoAddPolicy
import asyncio

app = FastAPI()

# Store active SSH sessions here
active_connections = {}

@app.websocket("/ws/{client_id}/{server_ip}")
async def websocket_endpoint(websocket: WebSocket, client_id: str, server_ip: str):
    await websocket.accept()
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        # Connect to the remote server via SSH
        ssh_client.connect(server_ip, username="your_username", password="your_password")
        active_connections[client_id] = ssh_client

        await websocket.send_text(f"Connected to {server_ip}.\n")

        while True:
            command = await websocket.receive_text()
            stdin, stdout, stderr = ssh_client.exec_command(command)

            # Stream the command's output back to the frontend
            for line in stdout:
                await websocket.send_text(line)
            for line in stderr:
                await websocket.send_text(f"Error: {line}")

    except Exception as e:
        await websocket.send_text(f"Connection failed: {str(e)}")
    finally:
        ssh_client.close()
        await websocket.close()
        active_connections.pop(client_id, None)
