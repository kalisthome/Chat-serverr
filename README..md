# WebSocket Chat Server

Simple WebSocket server using **aiohttp**, for live chat between clients.

## Usage

1. Run via Replit: import this repo.
2. Click **Run**, then connect Android WebSocket client to:  
   wss://<your-repl-name>.repl.co/ws

## Message format

```json
{"type": "chat", "nick": "Alice", "text": "Hello!"}
