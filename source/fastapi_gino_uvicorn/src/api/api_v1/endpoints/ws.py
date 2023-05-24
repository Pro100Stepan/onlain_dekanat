from typing import List
from main import app
from fastapi import  WebSocket, WebSocketDisconnect
from fastapi import APIRouter
import aiofiles
import base64

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, data: str, websocket: WebSocket):
        index = data
        async with aiofiles.open(f"./data/clouds_imgs/{index}.jpg", 'rb') as f:
            image = await f.read()
        base64img = base64.b64encode(image).decode('utf-8')
        await websocket.send_bytes(base64img)        
        # await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            websocket.app.logger.info(f'index={data}')
            await manager.send_personal_message(data, websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")
        
        
        
        
        
    