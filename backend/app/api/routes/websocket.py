from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.realtime.ws_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, receive pings if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
