import os
import json
from aiohttp import web

clients = set()

async def broadcast(data, sender):
    dead = []
    for c in list(clients):
        if c is not sender and not c.closed:
            try:
                await c.send_str(json.dumps(data))
            except Exception:
                dead.append(c)
    for d in dead:
        clients.discard(d)

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    print("Client connected:", request.remote)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    obj = json.loads(msg.data)
                except json.JSONDecodeError:
                    await ws.send_str(json.dumps({"type":"error","msg":"invalid json"}))
                    continue
                if obj.get("type") == "chat":
                    obj.setdefault("ts", None)
                    await broadcast(obj, ws)
            elif msg.type == web.WSMsgType.ERROR:
                print("WS error:", ws.exception())
    finally:
        clients.discard(ws)
        print("Client disconnected:", request.remote)
    return ws

async def http_ping(request):
    return web.Response(text="OK")

app = web.Application()
app.router.add_get('/', http_ping)
app.router.add_get('/ws', websocket_handler)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    web.run_app(app, host='0.0.0.0', port=port)
