import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import uvicorn

from PhysicsEngine import PhysicsEngine
from PolygonVertices import PolygonVertices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("physicserver")

app = FastAPI()

# Serve the web client files from /web at /static and expose index at /
app.mount("/static", StaticFiles(directory="web"), name="static")
from fastapi.responses import FileResponse


@app.get("/")
async def serve_index():
    return FileResponse("web/index.html")

physics = PhysicsEngine(time_step=1/60)
clients = set()

async def broadcast_state():
    state = physics.get_state()
    data = json.dumps({"type": "state", "payload": state})
    to_remove = []
    for ws in clients:
        try:
            await ws.send_text(data)
        except Exception:
            to_remove.append(ws)
    for ws in to_remove:
        clients.discard(ws)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    logger.info("WebSocket connection accepted: %s", websocket.client)
    try:
        while True:
            # handle any incoming messages with a short timeout so we can keep simulating
            try:
                msg = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
            except asyncio.TimeoutError:
                msg = None

            if msg is not None:
                logger.info("Received ws message from %s: %s", websocket.client, msg)
                try:
                    obj = json.loads(msg)
                    t = obj.get("type")
                    if t == "add_circle":
                        x = float(obj["x"])
                        y = float(obj["y"])
                        physics.add_body(position=[x, y], velocity=[0,0], mass=1, radius=20, color=(255,0,0))
                        logger.info("Added circle at %s,%s", x, y)
                    elif t == "add_polygon":
                        x = float(obj["x"])
                        y = float(obj["y"])
                        verts = PolygonVertices(int(obj.get("n",4)), float(obj.get("size",50)), 0)
                        physics.add_body(position=[x, y], velocity=[0,0], mass=1, radius=0, color=(255,0,0), vertices=verts)
                        logger.info("Added polygon at %s,%s (n=%s)", x, y, obj.get("n"))
                except Exception as ex:
                    logger.exception("Error handling ws message: %s", ex)
    except WebSocketDisconnect:
        clients.discard(websocket)

async def simulation_loop():
    dt = 1.0 / 60.0
    while True:
        physics.step(dt)
        await broadcast_state()
        await asyncio.sleep(dt)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulation_loop())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
